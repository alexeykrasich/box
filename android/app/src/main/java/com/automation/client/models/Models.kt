package com.automation.client.models

import com.google.gson.annotations.SerializedName

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: String?
)

data class AutomationType(
    val type: String,
    val name: String,
    val description: String,
    @SerializedName("config_schema")
    val configSchema: List<ConfigField>
)

data class ConfigField(
    val key: String,
    val label: String,
    val type: String,
    val required: Boolean,
    val default: String?,
    val options: List<String>?
)

data class Automation(
    val id: String,
    val name: String,
    val description: String,
    val status: String,
    val config: Map<String, Any>?,
    @SerializedName("last_run")
    val lastRun: String?,
    @SerializedName("error_message")
    val errorMessage: String?
)

data class CreateAutomationRequest(
    val type: String
)

data class StartAutomationRequest(
    val config: Map<String, String>
)

// Status constants
object AutomationStatus {
    const val STOPPED = "stopped"
    const val RUNNING = "running"
    const val ERROR = "error"
    const val SCHEDULED = "scheduled"
}

