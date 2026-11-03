package com.example.chamahub;

import android.graphics.Color;
import android.os.Bundle;
import android.view.Window;
import android.view.WindowInsetsController;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import androidx.fragment.app.Fragment;

import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity {
    private BottomNavigationView bottomNavigationView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Window window = getWindow();
        window.setStatusBarColor(Color.parseColor("#0066FF"));

        WindowInsetsControllerCompat controller = WindowCompat.getInsetsController(window, window.getDecorView());
        controller.setAppearanceLightStatusBars(false);

        bottomNavigationView = findViewById(R.id.bottomNav);

        if(savedInstanceState == null){
            loadFragment(new HomeFragment());
        }

        bottomNavigationView.setOnItemSelectedListener(item -> {
            Fragment selectedFragment;
            int itemId = item.getItemId();

            if (itemId == R.id.nav_home){
               selectedFragment = new HomeFragment();
            }else if(itemId == R.id.nav_contributions){
                selectedFragment = new ContributionsFragment();
            }else if(itemId == R.id.nav_loans){
                selectedFragment = new LoansFragment();
            }else if(itemId == R.id.nav_members){
                selectedFragment = new MembersFragment();
            }else {
                return false;
            }
            loadFragment(selectedFragment);
            return true;
        });

    }
    private void loadFragment(@NonNull Fragment fragment){
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.fragment_container, fragment)
                .commit();
    }
}