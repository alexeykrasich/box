package com.automation.client

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.automation.client.api.ApiClient
import com.automation.client.models.Automation
import com.automation.client.models.AutomationType
import com.automation.client.models.CreateAutomationRequest
import com.google.android.material.floatingactionbutton.FloatingActionButton
import io.socket.client.IO
import io.socket.client.Socket
import kotlinx.coroutines.launch
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: AutomationAdapter
    private lateinit var fab: FloatingActionButton
    private var socket: Socket? = null
    private var automationTypes: List<AutomationType> = emptyList()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Initialize API client
        ApiClient.initialize(this)
        
        // Setup RecyclerView
        recyclerView = findViewById(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        
        adapter = AutomationAdapter(
            automations = emptyList(),
            onStartClick = { automation -> showConfigDialog(automation) },
            onStopClick = { automation -> stopAutomation(automation) },
            onConfigClick = { automation -> openConfigActivity(automation) },
            onDeleteClick = { automation -> confirmDelete(automation) }
        )
        recyclerView.adapter = adapter
        
        // Setup FAB
        fab = findViewById(R.id.fab)
        fab.setOnClickListener { showAddAutomationDialog() }
        
        // Load data
        loadAutomationTypes()
        loadAutomations()
        
        // Connect to WebSocket
        connectWebSocket()
    }
    
    private fun loadAutomationTypes() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().getAutomationTypes()
                if (response.isSuccessful && response.body()?.success == true) {
                    automationTypes = response.body()?.data ?: emptyList()
                }
            } catch (e: Exception) {
                showError("Failed to load automation types: ${e.message}")
            }
        }
    }
    
    private fun loadAutomations() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().listAutomations()
                if (response.isSuccessful && response.body()?.success == true) {
                    val automations = response.body()?.data ?: emptyList()
                    adapter.updateAutomations(automations)
                } else {
                    showError("Failed to load automations")
                }
            } catch (e: Exception) {
                showError("Error: ${e.message}")
            }
        }
    }
    
    private fun showAddAutomationDialog() {
        if (automationTypes.isEmpty()) {
            showError("No automation types available")
            return
        }
        
        val types = automationTypes.map { it.name }.toTypedArray()
        AlertDialog.Builder(this)
            .setTitle("Add Automation")
            .setItems(types) { _, which ->
                createAutomation(automationTypes[which].type)
            }
            .show()
    }
    
    private fun createAutomation(type: String) {
        lifecycleScope.launch {
            try {
                val request = CreateAutomationRequest(type)
                val response = ApiClient.getApiService().createAutomation(request)
                if (response.isSuccessful && response.body()?.success == true) {
                    loadAutomations()
                    Toast.makeText(this@MainActivity, "Automation created", Toast.LENGTH_SHORT).show()
                } else {
                    showError("Failed to create automation")
                }
            } catch (e: Exception) {
                showError("Error: ${e.message}")
            }
        }
    }

    private fun showConfigDialog(automation: Automation) {
        openConfigActivity(automation)
    }

    private fun openConfigActivity(automation: Automation) {
        val intent = Intent(this, ConfigActivity::class.java)
        intent.putExtra("automation_id", automation.id)
        intent.putExtra("automation_name", automation.name)
        startActivity(intent)
    }

    private fun stopAutomation(automation: Automation) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().stopAutomation(automation.id)
                if (response.isSuccessful && response.body()?.success == true) {
                    Toast.makeText(this@MainActivity, "Automation stopped", Toast.LENGTH_SHORT).show()
                } else {
                    showError("Failed to stop automation")
                }
            } catch (e: Exception) {
                showError("Error: ${e.message}")
            }
        }
    }

    private fun confirmDelete(automation: Automation) {
        AlertDialog.Builder(this)
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
                if (response.isSuccessful && response.body()?.success == true) {
                    loadAutomations()
                    Toast.makeText(this@MainActivity, "Automation deleted", Toast.LENGTH_SHORT).show()
                } else {
                    showError("Failed to delete automation")
                }
            } catch (e: Exception) {
                showError("Error: ${e.message}")
            }
        }
    }

    private fun connectWebSocket() {
        try {
            val serverUrl = ApiClient.getServerUrl().removeSuffix("/")
            socket = IO.socket(serverUrl)

            socket?.on(Socket.EVENT_CONNECT) {
                runOnUiThread {
                    Toast.makeText(this, "Connected to server", Toast.LENGTH_SHORT).show()
                }
            }

            socket?.on("status_update") { args ->
                if (args.isNotEmpty()) {
                    val data = args[0] as JSONObject
                    runOnUiThread {
                        loadAutomations()
                    }
                }
            }

            socket?.on(Socket.EVENT_DISCONNECT) {
                runOnUiThread {
                    Toast.makeText(this, "Disconnected from server", Toast.LENGTH_SHORT).show()
                }
            }

            socket?.connect()
        } catch (e: Exception) {
            showError("WebSocket error: ${e.message}")
        }
    }

    private fun showError(message: String) {
        runOnUiThread {
            Toast.makeText(this, message, Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_refresh -> {
                loadAutomations()
                true
            }
            R.id.action_settings -> {
                startActivity(Intent(this, SettingsActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        socket?.disconnect()
    }

    override fun onResume() {
        super.onResume()
        loadAutomations()
    }
}
