package com.automation.client.fragments

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.automation.client.AutomationAdapter
import com.automation.client.ConfigActivity
import com.automation.client.R
import com.automation.client.api.ApiClient
import com.automation.client.models.Automation
import com.automation.client.models.AutomationType
import com.automation.client.models.CreateAutomationRequest
import kotlinx.coroutines.launch

class AutomationsFragment : Fragment() {
    
    private lateinit var recyclerView: RecyclerView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var emptyView: TextView
    private lateinit var adapter: AutomationAdapter
    private var automationTypes: List<AutomationType> = emptyList()
    
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_automations, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        recyclerView = view.findViewById(R.id.recyclerView)
        swipeRefresh = view.findViewById(R.id.swipeRefresh)
        emptyView = view.findViewById(R.id.emptyView)
        
        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        adapter = AutomationAdapter(
            automations = emptyList(),
            onStartClick = { openConfigActivity(it) },
            onStopClick = { stopAutomation(it) },
            onConfigClick = { openConfigActivity(it) },
            onDeleteClick = { confirmDelete(it) }
        )
        recyclerView.adapter = adapter
        
        swipeRefresh.setOnRefreshListener { loadData() }
        
        loadAutomationTypes()
        loadData()
    }
    
    private fun loadAutomationTypes() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().getAutomationTypes()
                if (response.isSuccessful && response.body()?.success == true) {
                    automationTypes = response.body()?.data ?: emptyList()
                }
            } catch (e: Exception) {
                // Ignore
            }
        }
    }
    
    fun loadData() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().listAutomations()
                if (response.isSuccessful && response.body()?.success == true) {
                    val automations = response.body()?.data ?: emptyList()
                    adapter.updateAutomations(automations)
                    emptyView.visibility = if (automations.isEmpty()) View.VISIBLE else View.GONE
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            } finally {
                swipeRefresh.isRefreshing = false
            }
        }
    }
    
    fun showAddDialog() {
        if (automationTypes.isEmpty()) {
            Toast.makeText(context, "No automation types available", Toast.LENGTH_SHORT).show()
            return
        }
        val types = automationTypes.map { it.name }.toTypedArray()
        AlertDialog.Builder(requireContext())
            .setTitle("Add Automation")
            .setItems(types) { _, which -> createAutomation(automationTypes[which].type) }
            .show()
    }
    
    private fun createAutomation(type: String) {
        lifecycleScope.launch {
            try {
                val request = CreateAutomationRequest(type)
                val response = ApiClient.getApiService().createAutomation(request)
                if (response.isSuccessful && response.body()?.success == true) {
                    loadData()
                    Toast.makeText(context, "Automation created", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun openConfigActivity(automation: Automation) {
        val intent = Intent(requireContext(), ConfigActivity::class.java)
        intent.putExtra("automation_id", automation.id)
        intent.putExtra("automation_name", automation.name)
        startActivity(intent)
    }
    
    private fun stopAutomation(automation: Automation) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().stopAutomation(automation.id)
                if (response.isSuccessful) {
                    loadData()
                    Toast.makeText(context, "Automation stopped", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun confirmDelete(automation: Automation) {
        AlertDialog.Builder(requireContext())
            .setTitle("Delete Automation")
            .setMessage("Are you sure you want to delete ${automation.name}?")
            .setPositiveButton("Delete") { _, _ -> deleteAutomation(automation) }
            .setNegativeButton("Cancel", null)
            .show()
    }
    
    private fun deleteAutomation(automation: Automation) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().deleteAutomation(automation.id)
                if (response.isSuccessful) {
                    loadData()
                    Toast.makeText(context, "Automation deleted", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    override fun onResume() {
        super.onResume()
        loadData()
    }
}

