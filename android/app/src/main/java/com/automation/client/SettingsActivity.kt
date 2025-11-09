package com.automation.client

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.automation.client.api.ApiClient

class SettingsActivity : AppCompatActivity() {
    
    private lateinit var serverUrlInput: EditText
    private lateinit var btnSave: Button
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)
        
        title = "Settings"
        
        serverUrlInput = findViewById(R.id.serverUrlInput)
        btnSave = findViewById(R.id.btnSaveSettings)
        
        // Load current server URL
        serverUrlInput.setText(ApiClient.getServerUrl())
        
        btnSave.setOnClickListener {
            saveSettings()
        }
    }
    
    private fun saveSettings() {
        val serverUrl = serverUrlInput.text.toString().trim()
        
        if (serverUrl.isEmpty()) {
            Toast.makeText(this, "Server URL cannot be empty", Toast.LENGTH_SHORT).show()
            return
        }
        
        // Ensure URL ends with /
        val formattedUrl = if (serverUrl.endsWith("/")) serverUrl else "$serverUrl/"
        
        ApiClient.setServerUrl(formattedUrl)
        Toast.makeText(this, "Settings saved. Please restart the app.", Toast.LENGTH_LONG).show()
        finish()
    }
}

