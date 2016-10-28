package com.example.rohitarunpathak.testingapplication;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import butterknife.Bind;
import butterknife.ButterKnife;


public class SplashActivity
        extends AppCompatActivity {

    private static final String TAG = "SplashActivity";


    @Bind(R.id.move_button)
    ImageView image_button;


    @Bind(R.id.progressBar1)
    ProgressBar spinner;

    @Bind(R.id.initial_info)
    TextView initialText;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "Creating");
        setContentView(R.layout.activity_splashscreen);
        ButterKnife.bind(this);
        Log.d(TAG, "Animating");

        new PrefetchData().execute();


    }

    private class PrefetchData extends AsyncTask<Void,String,Boolean> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();

            spinner.setVisibility(View.VISIBLE);
            float scale = getResources().getDisplayMetrics().density;
            int dpAsPixels = (int) (300*scale + 0.5f);

            spinner.setPadding(0,dpAsPixels,0,0);
            initialText.setText("Initializing...");

        }


        @Override
        protected Boolean doInBackground(Void... voids) {
            try {

                Thread.sleep(2000);
                publishProgress("Loading Profile...");

                Thread.sleep(5000);
                publishProgress("Almost Done...");

                Thread.sleep(1000);
                return true;
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            return false;
        }



        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            initialText.setText(values[0]);
        }

        @Override
        protected void onPostExecute(Boolean success) {

            if(success){
                initialText.setVisibility(View.GONE);
                spinner.setVisibility(View.GONE);
                spinner.setPadding(0,0,0,0);


                Intent intent = new Intent(SplashActivity.this, LoginActivity.class);
                startActivity(intent);
                finish();
                overridePendingTransition(R.anim.push_left_in, R.anim.push_left_out);
            }
        }


    }



}
