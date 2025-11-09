package com.automation.client.api

import com.automation.client.models.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    
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
}

