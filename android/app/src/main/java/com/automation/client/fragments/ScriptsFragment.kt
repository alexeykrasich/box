package com.automation.client.fragments

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
import com.automation.client.R
import com.automation.client.ScriptAdapter
import com.automation.client.api.ApiClient
import com.automation.client.models.Script
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class ScriptsFragment : Fragment() {
    
    private lateinit var recyclerView: RecyclerView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var emptyView: TextView
    private lateinit var adapter: ScriptAdapter
    
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_scripts, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        recyclerView = view.findViewById(R.id.recyclerView)
        swipeRefresh = view.findViewById(R.id.swipeRefresh)
        emptyView = view.findViewById(R.id.emptyView)
        
        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        adapter = ScriptAdapter(
            scripts = emptyList(),
            onRunClick = { confirmRunScript(it) }
        )
        recyclerView.adapter = adapter
        
        swipeRefresh.setOnRefreshListener { loadData() }
        
        loadData()
    }
    
    fun loadData() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().listScripts()
                if (response.isSuccessful && response.body()?.success == true) {
                    val scripts = response.body()?.data ?: emptyList()
                    adapter.updateScripts(scripts)
                    emptyView.visibility = if (scripts.isEmpty()) View.VISIBLE else View.GONE
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            } finally {
                swipeRefresh.isRefreshing = false
            }
        }
    }
    
    private fun confirmRunScript(script: Script) {
        AlertDialog.Builder(requireContext())
            .setTitle("Run Script")
            .setMessage("Run ${script.filename}?")
            .setPositiveButton("Run") { _, _ -> runScript(script) }
            .setNegativeButton("Cancel", null)
            .show()
    }
    
    private fun runScript(script: Script) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().runScript(script.filename)
                if (response.isSuccessful && response.body()?.success == true) {
                    val execution = response.body()?.data
                    Toast.makeText(context, "Script started: ${script.filename}", Toast.LENGTH_SHORT).show()
                    loadData()
                    
                    // Poll for completion
                    execution?.id?.let { runId ->
                        pollScriptStatus(runId, script.filename)
                    }
                } else {
                    Toast.makeText(context, "Failed to run script", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun pollScriptStatus(runId: String, filename: String) {
        lifecycleScope.launch {
            var attempts = 0
            while (attempts < 60) { // Poll for up to 60 seconds
                delay(1000)
                attempts++
                try {
                    val response = ApiClient.getApiService().getScriptStatus(runId)
                    if (response.isSuccessful && response.body()?.success == true) {
                        val status = response.body()?.data
                        if (status?.status != "running") {
                            loadData()
                            val message = when (status?.status) {
                                "completed" -> "Script completed: $filename"
                                "failed" -> "Script failed: $filename"
                                "error" -> "Script error: ${status.error}"
                                else -> "Script finished: $filename"
                            }
                            Toast.makeText(context, message, Toast.LENGTH_LONG).show()
                            
                            // Show output dialog if there's output
                            if (!status?.output.isNullOrEmpty()) {
                                showOutputDialog(filename, status?.output ?: "", status?.error ?: "")
                            }
                            break
                        }
                    }
                } catch (e: Exception) {
                    // Ignore polling errors
                }
            }
        }
    }
    
    private fun showOutputDialog(filename: String, output: String, error: String) {
        val message = buildString {
            if (output.isNotEmpty()) {
                append("Output:\n$output")
            }
            if (error.isNotEmpty()) {
                if (isNotEmpty()) append("\n\n")
                append("Errors:\n$error")
            }
        }
        
        if (message.isNotEmpty()) {
            AlertDialog.Builder(requireContext())
                .setTitle("Script Output: $filename")
                .setMessage(message.take(2000)) // Limit length
                .setPositiveButton("OK", null)
                .show()
        }
    }
    
    override fun onResume() {
        super.onResume()
        loadData()
    }
}

