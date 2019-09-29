package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity {
    public static final String UPLOAD_URL = "http://153.58.140.223:8080/upload.php";
    public static final String UPLOAD_KEY = "image";
    public static final String UPLOAD_URL2 = "http://153.58.140.223:5000/";
    public static final String UPLOAD_KEY2 = "image";

    public static final String USERNAME_KEY = "userName";
    static public Bitmap bitmap;
    private ImageView imageView;
    private int PICK_IMAGE_REQUEST = 1;
    private Uri filePath;


    private void showFileChooser() {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent, "Select Picture"), PICK_IMAGE_REQUEST);
        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new
                    StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && data != null && data.getData() != null) {

            filePath = data.getData();
            try {
                bitmap = MediaStore.Images.Media.getBitmap(getApplicationContext().getContentResolver(), filePath);
                imageView.setImageBitmap(bitmap);
                uploadImage();
                ackServer();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public String getStringImage(Bitmap bmp){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] imageBytes = baos.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;
    }

    private void ackServer(){
        class AckServer extends AsyncTask<Bitmap,Void,String> {

            ProgressDialog loading;
            RequestHandler rh = new RequestHandler();

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                Toast.makeText(getApplicationContext(),"About to Ack Server",Toast.LENGTH_SHORT).show();
                Log.d("info", "about to ack server");

            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);

                Toast.makeText(getApplicationContext(),"to Ack Server",Toast.LENGTH_SHORT).show();
                Log.d("info", "to Ack Server");
            }

            @Override
            protected String doInBackground(Bitmap... params) {
                Bitmap bitmap = params[0];
                String uploadImage = getStringImage(bitmap);

                HashMap<String,String> data = new HashMap<>();

                data.put(UPLOAD_KEY, "hello");
                // data.put("files", uploadImage);
                String result = rh.sendPostRequest(UPLOAD_URL2,data);
                Log.d("info", "Ack Server Done");
                return result;
            }
        }

        AckServer ui = new AckServer();
        ui.execute(bitmap);
    }


    private void uploadImage(){
        class UploadImage extends AsyncTask<Bitmap,Void,String> {

            ProgressDialog loading;
            RequestHandler rh = new RequestHandler();

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                Toast.makeText(getApplicationContext(),"About to Uploaded image",Toast.LENGTH_SHORT).show();
                Log.d("info", "about to upload image");

            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);

                Toast.makeText(getApplicationContext(),"Uploaded image",Toast.LENGTH_SHORT).show();
                Log.d("info", "uploaded image");
            }

            @Override
            protected String doInBackground(Bitmap... params) {
                Bitmap bitmap = params[0];
                String uploadImage = getStringImage(bitmap);

                HashMap<String,String> data = new HashMap<>();

                data.put(UPLOAD_KEY, uploadImage);
                data.put("files", uploadImage);
                String result = rh.sendPostRequest(UPLOAD_URL,data);
                Log.d("info", "uploading image");
                return result;
            }
        }

        UploadImage ui = new UploadImage();
        ui.execute(bitmap);
        imageView.setImageBitmap(bitmap);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView = findViewById(R.id.imageView);


        final Button button = (Button) findViewById(R.id.submit);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // your handler code here
                //Displaying Toast with Hello Javatpoint message
                Toast.makeText(getApplicationContext(),"Send image",Toast.LENGTH_SHORT).show();

                showFileChooser();

            }
        });
    }
}
