package com.automation.client

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.automation.client.models.DockerContainer
import com.google.android.material.button.MaterialButton

class DockerAdapter(
    private var containers: List<DockerContainer>,
    private val onToggleClick: (DockerContainer) -> Unit,
    private val onLongClick: (DockerContainer) -> Unit
) : RecyclerView.Adapter<DockerAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val statusIndicator: View = view.findViewById(R.id.statusIndicator)
        val txtContainerName: TextView = view.findViewById(R.id.txtContainerName)
        val txtImage: TextView = view.findViewById(R.id.txtImage)
        val txtStatus: TextView = view.findViewById(R.id.txtStatus)
        val txtPorts: TextView = view.findViewById(R.id.txtPorts)
        val btnToggle: MaterialButton = view.findViewById(R.id.btnToggle)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_docker, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val container = containers[position]
        
        holder.txtContainerName.text = container.name
        holder.txtImage.text = "Image: ${container.image}"
        holder.txtStatus.text = container.status
        
        // Status indicator color
        val statusColor = if (container.isRunning) {
            Color.parseColor("#4CAF50") // Green
        } else {
            Color.parseColor("#F44336") // Red
        }
        holder.statusIndicator.setBackgroundColor(statusColor)
        
        // Toggle button
        if (container.isRunning) {
            holder.btnToggle.text = "Stop"
        } else {
            holder.btnToggle.text = "Start"
        }
        
        // Show ports if available
        if (container.ports.isNotEmpty()) {
            holder.txtPorts.visibility = View.VISIBLE
            holder.txtPorts.text = "Ports: ${container.ports}"
        } else {
            holder.txtPorts.visibility = View.GONE
        }
        
        holder.btnToggle.setOnClickListener { onToggleClick(container) }
        holder.itemView.setOnLongClickListener { 
            onLongClick(container)
            true
        }
    }

    override fun getItemCount() = containers.size

    fun updateContainers(newContainers: List<DockerContainer>) {
        containers = newContainers
        notifyDataSetChanged()
    }
}

