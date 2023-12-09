package com.example.myapplication

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.myapplication.databinding.ActivityLoginBinding

const val REQUEST_CODE_SIGN_IN = 0

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        binding = ActivityLoginBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)


        val intent = intent
        val strName = intent.getStringExtra("name")
        val strNum = intent.getStringExtra("number")
        val user = intent.getStringExtra("user")

        binding.textView5.text = user

        binding.textView4.text = strName

        if(intent.getBooleanExtra("checked", false)){
            binding.textView3.text = "The user selected the checkbox"
        } else {
            binding.textView3.text = "brrrrrrrrrrrrrrrrrrrap"
        }

        binding.button2.text = strNum

        //binding.textView3.text = intent.getStringExtra("name")


        //val displayName = findViewById<TextView>(R.id.textView3)
        //displayName.text = intent.getStringExtra("name")
    }


}