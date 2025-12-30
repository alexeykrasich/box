package com.automation.client

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.automation.client.models.Automation
import com.automation.client.models.AutomationStatus

class AutomationAdapter(
    private var automations: List<Automation>,
    private val onStartClick: (Automation) -> Unit,
    private val onStopClick: (Automation) -> Unit,
    private val onConfigClick: (Automation) -> Unit,
    private val onDeleteClick: (Automation) -> Unit
) : RecyclerView.Adapter<AutomationAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val nameText: TextView = view.findViewById(R.id.automationName)
        val statusText: TextView = view.findViewById(R.id.automationStatus)
        val descriptionText: TextView = view.findViewById(R.id.automationDescription)
        val lastRunText: TextView = view.findViewById(R.id.lastRun)
        val errorText: TextView = view.findViewById(R.id.errorMessage)
        val startButton: Button = view.findViewById(R.id.btnStart)
        val stopButton: Button = view.findViewById(R.id.btnStop)
        val configButton: Button = view.findViewById(R.id.btnConfig)
        val deleteButton: Button = view.findViewById(R.id.btnDelete)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_automation, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val automation = automations[position]
        
        holder.nameText.text = automation.name
        holder.descriptionText.text = automation.description
        holder.statusText.text = "Status: ${automation.status.uppercase()}"
        
        // Set status color
        when (automation.status) {
            AutomationStatus.RUNNING -> holder.statusText.setTextColor(Color.parseColor("#4CAF50"))
            AutomationStatus.STOPPED -> holder.statusText.setTextColor(Color.parseColor("#9E9E9E"))
            AutomationStatus.ERROR -> holder.statusText.setTextColor(Color.parseColor("#F44336"))
            else -> holder.statusText.setTextColor(Color.parseColor("#2196F3"))
        }
        
        // Last run
        if (automation.lastRun != null) {
            holder.lastRunText.visibility = View.VISIBLE
            holder.lastRunText.text = "Last run: ${automation.lastRun}"
        } else {
            holder.lastRunText.visibility = View.GONE
        }
        
        // Error message
        if (automation.errorMessage != null) {
            holder.errorText.visibility = View.VISIBLE
            holder.errorText.text = "Error: ${automation.errorMessage}"
        } else {
            holder.errorText.visibility = View.GONE
        }
        
        // Button states
        val isRunning = automation.status == AutomationStatus.RUNNING
        holder.startButton.isEnabled = !isRunning
        holder.stopButton.isEnabled = isRunning
        holder.configButton.isEnabled = !isRunning
        
        // Button clicks
        holder.startButton.setOnClickListener { onStartClick(automation) }
        holder.stopButton.setOnClickListener { onStopClick(automation) }
        holder.configButton.setOnClickListener { onConfigClick(automation) }
        holder.deleteButton.setOnClickListener { onDeleteClick(automation) }
    }

    override fun getItemCount() = automations.size

    fun updateAutomations(newAutomations: List<Automation>) {
        automations = newAutomations
        notifyDataSetChanged()
    }
    
    fun updateAutomation(automation: Automation) {
        val index = automations.indexOfFirst { it.id == automation.id }
        if (index != -1) {
            automations = automations.toMutableList().apply { set(index, automation) }
            notifyItemChanged(index)
        }
    }
}

