package com.automation.client.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.automation.client.DockerAdapter
import com.automation.client.R
import com.automation.client.api.ApiClient
import com.automation.client.models.DockerContainer
import kotlinx.coroutines.launch

class DockerFragment : Fragment() {
    
    private lateinit var recyclerView: RecyclerView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var emptyView: TextView
    private lateinit var dockerUnavailableView: LinearLayout
    private lateinit var adapter: DockerAdapter
    private var dockerAvailable = false
    
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_docker, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        recyclerView = view.findViewById(R.id.recyclerView)
        swipeRefresh = view.findViewById(R.id.swipeRefresh)
        emptyView = view.findViewById(R.id.emptyView)
        dockerUnavailableView = view.findViewById(R.id.dockerUnavailableView)
        
        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        adapter = DockerAdapter(
            containers = emptyList(),
            onToggleClick = { toggleContainer(it) },
            onLongClick = { showContainerMenu(it) }
        )
        recyclerView.adapter = adapter
        
        swipeRefresh.setOnRefreshListener { loadData() }
        
        checkDockerStatus()
    }
    
    private fun checkDockerStatus() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().getDockerStatus()
                if (response.isSuccessful && response.body()?.success == true) {
                    dockerAvailable = response.body()?.data?.available ?: false
                    if (dockerAvailable) {
                        dockerUnavailableView.visibility = View.GONE
                        loadData()
                    } else {
                        dockerUnavailableView.visibility = View.VISIBLE
                        recyclerView.visibility = View.GONE
                    }
                }
            } catch (e: Exception) {
                dockerUnavailableView.visibility = View.VISIBLE
                recyclerView.visibility = View.GONE
            } finally {
                swipeRefresh.isRefreshing = false
            }
        }
    }
    
    fun loadData() {
        if (!dockerAvailable) {
            checkDockerStatus()
            return
        }
        
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().listContainers()
                if (response.isSuccessful && response.body()?.success == true) {
                    val containers = response.body()?.data ?: emptyList()
                    adapter.updateContainers(containers)
                    recyclerView.visibility = View.VISIBLE
                    emptyView.visibility = if (containers.isEmpty()) View.VISIBLE else View.GONE
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            } finally {
                swipeRefresh.isRefreshing = false
            }
        }
    }
    
    private fun toggleContainer(container: DockerContainer) {
        lifecycleScope.launch {
            try {
                val response = if (container.isRunning) {
                    ApiClient.getApiService().stopContainer(container.id)
                } else {
                    ApiClient.getApiService().startContainer(container.id)
                }
                
                if (response.isSuccessful && response.body()?.success == true) {
                    val action = if (container.isRunning) "stopped" else "started"
                    Toast.makeText(context, "Container $action: ${container.name}", Toast.LENGTH_SHORT).show()
                    loadData()
                } else {
                    Toast.makeText(context, "Failed to toggle container", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun showContainerMenu(container: DockerContainer) {
        val options = arrayOf("Restart", "View Logs")
        AlertDialog.Builder(requireContext())
            .setTitle(container.name)
            .setItems(options) { _, which ->
                when (which) {
                    0 -> restartContainer(container)
                    1 -> viewLogs(container)
                }
            }
            .show()
    }
    
    private fun restartContainer(container: DockerContainer) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().restartContainer(container.id)
                if (response.isSuccessful) {
                    Toast.makeText(context, "Container restarted: ${container.name}", Toast.LENGTH_SHORT).show()
                    loadData()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun viewLogs(container: DockerContainer) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().getContainerLogs(container.id)
                if (response.isSuccessful && response.body()?.success == true) {
                    val logs = response.body()?.data?.logs ?: "No logs available"
                    AlertDialog.Builder(requireContext())
                        .setTitle("Logs: ${container.name}")
                        .setMessage(logs.takeLast(3000))
                        .setPositiveButton("OK", null)
                        .show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    override fun onResume() {
        super.onResume()
        if (dockerAvailable) loadData() else checkDockerStatus()
    }
}

