package com.automation.client.api

import com.automation.client.models.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // ============== AUTOMATIONS API ==============

    @GET("api/automations/types")
    suspend fun getAutomationTypes(): Response<ApiResponse<List<AutomationType>>>

    @GET("api/automations")
    suspend fun listAutomations(): Response<ApiResponse<List<Automation>>>

    @POST("api/automations")
    suspend fun createAutomation(@Body request: CreateAutomationRequest): Response<ApiResponse<Automation>>

    @GET("api/automations/{id}")
    suspend fun getAutomation(@Path("id") id: String): Response<ApiResponse<Automation>>

    @POST("api/automations/{id}/start")
    suspend fun startAutomation(
        @Path("id") id: String,
        @Body request: StartAutomationRequest
    ): Response<ApiResponse<Automation>>

    @POST("api/automations/{id}/stop")
    suspend fun stopAutomation(@Path("id") id: String): Response<ApiResponse<Automation>>

    @DELETE("api/automations/{id}")
    suspend fun deleteAutomation(@Path("id") id: String): Response<ApiResponse<Unit>>

    // ============== SCRIPTS API ==============

    @GET("api/scripts")
    suspend fun listScripts(): Response<ApiResponse<List<Script>>>

    @POST("api/scripts/{filename}/run")
    suspend fun runScript(@Path("filename") filename: String): Response<ApiResponse<ScriptExecution>>

    @GET("api/scripts/running")
    suspend fun getRunningScripts(): Response<ApiResponse<List<ScriptExecution>>>

    @GET("api/scripts/status/{runId}")
    suspend fun getScriptStatus(@Path("runId") runId: String): Response<ApiResponse<ScriptExecution>>

    @POST("api/scripts/stop/{runId}")
    suspend fun stopScript(@Path("runId") runId: String): Response<ApiResponse<ScriptExecution>>

    // ============== DOCKER API ==============

    @GET("api/docker/status")
    suspend fun getDockerStatus(): Response<ApiResponse<DockerStatus>>

    @GET("api/docker/containers")
    suspend fun listContainers(@Query("all") all: Boolean = true): Response<ApiResponse<List<DockerContainer>>>

    @POST("api/docker/containers/{id}/start")
    suspend fun startContainer(@Path("id") containerId: String): Response<ApiResponse<DockerAction>>

    @POST("api/docker/containers/{id}/stop")
    suspend fun stopContainer(@Path("id") containerId: String): Response<ApiResponse<DockerAction>>

    @POST("api/docker/containers/{id}/restart")
    suspend fun restartContainer(@Path("id") containerId: String): Response<ApiResponse<DockerAction>>

    @GET("api/docker/containers/{id}/logs")
    suspend fun getContainerLogs(
        @Path("id") containerId: String,
        @Query("tail") tail: Int = 100
    ): Response<ApiResponse<ContainerLogs>>
}

