package com.automation.client

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.viewpager2.widget.ViewPager2
import com.automation.client.api.ApiClient
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.tabs.TabLayout
import com.google.android.material.tabs.TabLayoutMediator
import io.socket.client.IO
import io.socket.client.Socket
import org.json.JSONObject

class MainActivity : AppCompatActivity() {

    private lateinit var tabLayout: TabLayout
    private lateinit var viewPager: ViewPager2
    private lateinit var fab: FloatingActionButton
    private lateinit var pagerAdapter: MainPagerAdapter
    private var socket: Socket? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize API client
        ApiClient.initialize(this)

        // Setup ViewPager with tabs
        tabLayout = findViewById(R.id.tabLayout)
        viewPager = findViewById(R.id.viewPager)
        fab = findViewById(R.id.fab)

        pagerAdapter = MainPagerAdapter(this)
        viewPager.adapter = pagerAdapter

        TabLayoutMediator(tabLayout, viewPager) { tab, position ->
            tab.text = pagerAdapter.getTabTitle(position)
        }.attach()

        // Setup FAB - show only on Automations tab
        fab.setOnClickListener { onFabClick() }

        viewPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                // Show FAB only on Automations tab
                fab.visibility = if (position == 0) View.VISIBLE else View.GONE
            }
        })

        // Connect to WebSocket
        connectWebSocket()
    }

    private fun onFabClick() {
        when (viewPager.currentItem) {
            0 -> pagerAdapter.automationsFragment.showAddDialog()
        }
    }

    private fun connectWebSocket() {
        try {
            val serverUrl = ApiClient.getServerUrl().removeSuffix("/")
            socket = IO.socket(serverUrl)

            socket?.on(Socket.EVENT_CONNECT) {
                runOnUiThread {
                    Toast.makeText(this, "Connected to server", Toast.LENGTH_SHORT).show()
                }
            }

            socket?.on("status_update") { args ->
                if (args.isNotEmpty()) {
                    @Suppress("UNUSED_VARIABLE")
                    val data = args[0] as JSONObject
                    runOnUiThread {
                        refreshCurrentTab()
                    }
                }
            }

            socket?.on(Socket.EVENT_DISCONNECT) {
                runOnUiThread {
                    Toast.makeText(this, "Disconnected from server", Toast.LENGTH_SHORT).show()
                }
            }

            socket?.connect()
        } catch (e: Exception) {
            Toast.makeText(this, "WebSocket error: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    private fun refreshCurrentTab() {
        when (viewPager.currentItem) {
            0 -> pagerAdapter.automationsFragment.loadData()
            1 -> pagerAdapter.scriptsFragment.loadData()
            2 -> pagerAdapter.dockerFragment.loadData()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_refresh -> {
                refreshCurrentTab()
                true
            }
            R.id.action_settings -> {
                startActivity(Intent(this, SettingsActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        socket?.disconnect()
    }
}
