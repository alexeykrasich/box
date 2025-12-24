package com.automation.client

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter
import com.automation.client.fragments.AutomationsFragment
import com.automation.client.fragments.DockerFragment
import com.automation.client.fragments.ScriptsFragment

class MainPagerAdapter(activity: FragmentActivity) : FragmentStateAdapter(activity) {
    
    val automationsFragment = AutomationsFragment()
    val scriptsFragment = ScriptsFragment()
    val dockerFragment = DockerFragment()
    
    override fun getItemCount(): Int = 3
    
    override fun createFragment(position: Int): Fragment {
        return when (position) {
            0 -> automationsFragment
            1 -> scriptsFragment
            2 -> dockerFragment
            else -> automationsFragment
        }
    }
    
    fun getTabTitle(position: Int): String {
        return when (position) {
            0 -> "Automations"
            1 -> "Scripts"
            2 -> "Docker"
            else -> ""
        }
    }
}

