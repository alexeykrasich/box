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

// ============== SCRIPTS MODELS ==============

data class Script(
    val filename: String,
    val path: String,
    val extension: String,
    val size: Long,
    val modified: String,
    @SerializedName("is_running")
    val isRunning: Boolean
)

data class ScriptExecution(
    val id: String,
    val filename: String,
    val status: String,
    @SerializedName("started_at")
    val startedAt: String?,
    @SerializedName("finished_at")
    val finishedAt: String?,
    val output: String?,
    val error: String?,
    @SerializedName("return_code")
    val returnCode: Int?
)

// ============== DOCKER MODELS ==============

data class DockerStatus(
    val available: Boolean,
    val error: String?
)

data class DockerContainer(
    val id: String,
    val name: String,
    val image: String,
    val status: String,
    val state: String,
    val ports: String,
    val created: String,
    @SerializedName("is_running")
    val isRunning: Boolean
)

data class DockerAction(
    val success: Boolean,
    @SerializedName("container_id")
    val containerId: String,
    val action: String,
    val message: String
)

data class ContainerLogs(
    @SerializedName("container_id")
    val containerId: String,
    val logs: String,
    val success: Boolean
)

