package com.example.rohitarunpathak.testingapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

/**
 * Created by rohit.arun.pathak on 10/25/2016.
 */

public class SplashScreen extends Activity {

    private static int SPLASH_TIME_OUT=3000;
    LinearLayout register_layout;
    LinearLayout internet_missing;
    LinearLayout login_layout;
    LinearLayout footer_layout;
    TextView register_text;
    private ProgressBar spinner;


    Button register_btn;
    Button login_button;
    ImageButton image_button;

    TextView initialText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        login_layout = (LinearLayout)findViewById(R.id.login_layout);
        login_layout.setVisibility(View.GONE);

        register_layout = (LinearLayout)findViewById(R.id.register_layout);
        register_layout.setVisibility(View.GONE);

        internet_missing = (LinearLayout)findViewById(R.id.internet_retry);
        internet_missing.setVisibility(View.GONE);

        footer_layout = (LinearLayout)findViewById(R.id.footer_layout);
        footer_layout.setVisibility(View.GONE);

        image_button = (ImageButton) findViewById(R.id.move_button);

        login_button=(Button)findViewById(R.id.login_btn);
        login_button.setOnClickListener(new OnLoginButtonClick());

        spinner = (ProgressBar)findViewById(R.id.progressBar1);

        initialText=(TextView)findViewById(R.id.initial_info);

        new PrefetchData().execute();


    }
    /** Async task to make http call*/

    private class PrefetchData extends AsyncTask<Void,String,Boolean>{

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
                Animation logoanimation=AnimationUtils.loadAnimation(SplashScreen.this,R.anim.splash_anim);
                image_button.startAnimation(logoanimation);

                image_button.postOnAnimationDelayed(new Runnable() {
                    @Override
                    public void run() {
                        login_layout.setVisibility(View.VISIBLE);
                        footer_layout.setVisibility(View.VISIBLE);
                    }
                },1000);

            }
        }


    }

    private class OnLoginButtonClick implements View.OnClickListener {

        @Override
        public void onClick(View view) {
            PerformTimeConsumingOperation();
            new GetData().execute();
        }

        private void PerformTimeConsumingOperation() {

                Intent localIntent=new Intent(SplashScreen.this,DemoActivity.class);
                startActivity(localIntent);
                finish();


        }


        private class GetData extends AsyncTask<Void,Void,Boolean>{
            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                StartAnimation();

            }

            private void StartAnimation() {

                spinner.setVisibility(View.VISIBLE);
                Log.d("Training Application","Starting Animation");
            }

            @Override
            protected Boolean doInBackground(Void... voids) {
                try {
                    Thread.sleep(5000);
                    return true;
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                return false;
            }

            @Override
            protected void onPostExecute(Boolean aBoolean) {
                super.onPostExecute(aBoolean);

                if(aBoolean){
                    spinner.setVisibility(View.GONE);
                }
            }
        }
    }
}
