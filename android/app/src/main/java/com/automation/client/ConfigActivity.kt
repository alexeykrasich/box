package com.automation.client

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.automation.client.api.ApiClient
import com.automation.client.models.AutomationType
import com.automation.client.models.ConfigField
import com.automation.client.models.StartAutomationRequest
import kotlinx.coroutines.launch
import java.util.*

class ConfigActivity : AppCompatActivity() {
    
    private lateinit var automationId: String
    private lateinit var automationName: String
    private lateinit var configContainer: LinearLayout
    private lateinit var btnStart: Button
    private val configValues = mutableMapOf<String, String>()
    private var configSchema: List<ConfigField> = emptyList()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_config)
        
        automationId = intent.getStringExtra("automation_id") ?: ""
        automationName = intent.getStringExtra("automation_name") ?: ""
        
        title = "Configure $automationName"
        
        configContainer = findViewById(R.id.configContainer)
        btnStart = findViewById(R.id.btnStartAutomation)
        
        btnStart.setOnClickListener {
            startAutomation()
        }
        
        loadConfigSchema()
    }
    
    private fun loadConfigSchema() {
        lifecycleScope.launch {
            try {
                val response = ApiClient.getApiService().getAutomationTypes()
                if (response.isSuccessful && response.body()?.success == true) {
                    val types = response.body()?.data ?: emptyList()
                    
                    // Find the automation type
                    val automationType = types.find { type ->
                        type.name == automationName
                    }
                    
                    if (automationType != null) {
                        configSchema = automationType.configSchema
                        buildConfigForm()
                    }
                }
            } catch (e: Exception) {
                showError("Failed to load config: ${e.message}")
            }
        }
    }
    
    private fun buildConfigForm() {
        configContainer.removeAllViews()
        
        for (field in configSchema) {
            val fieldView = createFieldView(field)
            configContainer.addView(fieldView)
        }
    }
    
    private fun createFieldView(field: ConfigField): View {
        val container = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(16, 16, 16, 16)
        }
        
        // Label
        val label = TextView(this).apply {
            text = field.label + if (field.required) " *" else ""
            textSize = 16f
            setPadding(0, 0, 0, 8)
        }
        container.addView(label)
        
        // Input field based on type
        when (field.type) {
            "text" -> {
                val editText = EditText(this).apply {
                    hint = field.default ?: ""
                    setText(field.default ?: "")
                    addTextChangedListener(object : android.text.TextWatcher {
                        override fun afterTextChanged(s: android.text.Editable?) {
                            configValues[field.key] = s.toString()
                        }
                        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
                    })
                }
                container.addView(editText)
                configValues[field.key] = field.default ?: ""
            }
            
            "number" -> {
                val editText = EditText(this).apply {
                    hint = field.default ?: ""
                    setText(field.default ?: "")
                    inputType = android.text.InputType.TYPE_CLASS_NUMBER
                    addTextChangedListener(object : android.text.TextWatcher {
                        override fun afterTextChanged(s: android.text.Editable?) {
                            configValues[field.key] = s.toString()
                        }
                        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
                    })
                }
                container.addView(editText)
                configValues[field.key] = field.default ?: ""
            }
            
            "date" -> {
                val button = Button(this).apply {
                    text = field.default ?: "Select Date"
                    setOnClickListener {
                        showDatePicker(field.key, this)
                    }
                }
                container.addView(button)
            }
            
            "time" -> {
                val button = Button(this).apply {
                    text = field.default ?: "Select Time"
                    setOnClickListener {
                        showTimePicker(field.key, this)
                    }
                }
                container.addView(button)
                configValues[field.key] = field.default ?: ""
            }
        }

        return container
    }

    private fun showDatePicker(key: String, button: Button) {
        val calendar = Calendar.getInstance()
        val datePickerDialog = DatePickerDialog(
            this,
            { _, year, month, dayOfMonth ->
                val date = String.format("%04d-%02d-%02d", year, month + 1, dayOfMonth)
                button.text = date
                configValues[key] = date
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH)
        )
        datePickerDialog.show()
    }

    private fun showTimePicker(key: String, button: Button) {
        val calendar = Calendar.getInstance()
        val timePickerDialog = TimePickerDialog(
            this,
            { _, hourOfDay, minute ->
                val time = String.format("%02d:%02d", hourOfDay, minute)
                button.text = time
                configValues[key] = time
            },
            calendar.get(Calendar.HOUR_OF_DAY),
            calendar.get(Calendar.MINUTE),
            true
        )
        timePickerDialog.show()
    }

    private fun startAutomation() {
        // Validate required fields
        for (field in configSchema) {
            if (field.required && configValues[field.key].isNullOrBlank()) {
                showError("${field.label} is required")
                return
            }
        }

        lifecycleScope.launch {
            try {
                val request = StartAutomationRequest(configValues)
                val response = ApiClient.getApiService().startAutomation(automationId, request)

                if (response.isSuccessful && response.body()?.success == true) {
                    Toast.makeText(this@ConfigActivity, "Automation started", Toast.LENGTH_SHORT).show()
                    finish()
                } else {
                    showError("Failed to start automation: ${response.body()?.error}")
                }
            } catch (e: Exception) {
                showError("Error: ${e.message}")
            }
        }
    }

    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show()
    }
}

