package com.automation.client

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.ProgressBar
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.automation.client.models.Script
import com.google.android.material.button.MaterialButton

class ScriptAdapter(
    private var scripts: List<Script>,
    private val onRunClick: (Script) -> Unit
) : RecyclerView.Adapter<ScriptAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val iconScript: ImageView = view.findViewById(R.id.iconScript)
        val txtFilename: TextView = view.findViewById(R.id.txtFilename)
        val txtInfo: TextView = view.findViewById(R.id.txtInfo)
        val progressBar: ProgressBar = view.findViewById(R.id.progressBar)
        val btnRun: MaterialButton = view.findViewById(R.id.btnRun)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_script, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val script = scripts[position]
        
        holder.txtFilename.text = script.filename
        
        val sizeKb = script.size / 1024.0
        holder.txtInfo.text = String.format("%.1f KB • %s", sizeKb, script.extension.uppercase())
        
        // Set icon based on script type
        val iconRes = when (script.extension) {
            ".py" -> android.R.drawable.ic_menu_edit
            ".sh", ".bash" -> android.R.drawable.ic_menu_manage
            else -> android.R.drawable.ic_menu_agenda
        }
        holder.iconScript.setImageResource(iconRes)
        
        // Show running state
        if (script.isRunning) {
            holder.progressBar.visibility = View.VISIBLE
            holder.btnRun.text = "Running..."
            holder.btnRun.isEnabled = false
        } else {
            holder.progressBar.visibility = View.GONE
            holder.btnRun.text = "Run"
            holder.btnRun.isEnabled = true
        }
        
        holder.btnRun.setOnClickListener { onRunClick(script) }
        holder.itemView.setOnClickListener { onRunClick(script) }
    }

    override fun getItemCount() = scripts.size

    fun updateScripts(newScripts: List<Script>) {
        scripts = newScripts
        notifyDataSetChanged()
    }
}

