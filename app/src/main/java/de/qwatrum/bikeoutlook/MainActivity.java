package de.qwatrum.bikeoutlook;

import android.app.Dialog;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;

import com.google.android.material.snackbar.Snackbar;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.util.Log;
import android.view.Gravity;
import android.view.View;

import androidx.core.content.res.ResourcesCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import de.qwatrum.bikeoutlook.databinding.ActivityMainBinding;

import android.view.Menu;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.osmdroid.api.IMapController;
import org.osmdroid.config.Configuration;
import org.osmdroid.tileprovider.tilesource.TileSourceFactory;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.views.MapController;
import org.osmdroid.views.overlay.Marker;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private MapView mapView;
    private IMapController mapController;

    private final String TAG = "BikeOutlook";
    private final OkHttpClient client = new OkHttpClient();
    private AppBarConfiguration appBarConfiguration;
    private ActivityMainBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);

        Configuration.getInstance().setUserAgentValue(getPackageName());

        File basePath = new File(getCacheDir(), "osmdroid");
        Configuration.getInstance().setOsmdroidBasePath(basePath);
        Configuration.getInstance().setOsmdroidTileCache(new File(basePath, "tiles"));

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        mapView = findViewById(R.id.map);

        mapView.setTileSource(TileSourceFactory.MAPNIK);

        mapView.setMultiTouchControls(true);
        mapView.setMaxZoomLevel(20.0);
        mapView.setMinZoomLevel(11.5);
        mapView.setScrollableAreaLimitLatitude(52.4536, 52.3121, 0);
        mapView.setScrollableAreaLimitLongitude(9.6244, 9.9125, 0);

        mapController = mapView.getController();
        mapController.setZoom(12.5);

        GeoPoint startPoint = new GeoPoint(52.38884, 9.7068811);
        mapController.setCenter(startPoint);

        String[] stations = {"306149925!Hauptbahnhof Süd!52.376343!9.740046", "306150652!Hauptbahnhof Nord!52.377525!9.744294", "306151680!Raschplatz!52.379661!9.744232", "306152946!Limmerstraße/Offensteinstraße!52.374238!9.705778", "306153381!Am Küchengarten!52.370949!9.714468", "306154042!Leibnitz Universität/Nienburger Straße!52.38097!9.718986", "306155298!Callinstraße!52.386635!9.71494", "306155771!Appelstraße!52.389201!9.712794", "306157005!Lister Platz!52.388491!9.750946", "306157498!Georgstraße!52.37523!9.734664", "306159446!Marienstraße!52.370098!9.752518", "306424741!Sprengel Museum!52.364224!9.739798", "306426180!Am Klagesmarkt!52.380791!9.726797", "306427898!Sedanstraße/Lister Meile!52.383795!9.746338", "306427940!Kurt-Schumacher-Straße!52.376915!9.736471", "306429471!Königsworther Platz!52.378471!9.723067", "306429774!Schwarzer Bär!52.368157!9.719423", "306430168!Schneiderberg/Wilhelm-Busch-Museum!52.384996!9.712872", "306430513!Kopernikusstraße!52.386821!9.723689", "306432156!Limmerstraße/Freizeitheim Linden!52.375321!9.700005", "306434837!Nikolaistraße!52.380099!9.732867", "306435831!Opernplatz!52.37368!9.739299", "306436482!Karmarschstraße!52.372394!9.737738", "306437759!Aegidientorplatz Süd!52.36783!9.742566", "306584215!Sallplatz!52.36182!9.759264", "306586739!Schlägerstraße!52.365587!9.7466", "306589353!Geibelstraße!52.359235!9.751621", "306591040!Glocksee/Braunstraße!52.373171!9.720738", "306592207!Hahnenstraße!52.386136!9.718007", "306608230!Herrenhäuser Kirchweg!52.390861!9.705861", "306611557!Engelbosteler Damm!52.390409!9.720819", "306612767!Scheffelstraße!52.384019!9.725321", "306614385!Im Moore!52.383659!9.720906", "306615251!Werderstraße!52.387351!9.733565", "306616745!Vahrenwalder Platz!52.391093!9.73438", "306618340!Niedersachsenring!52.399116!9.737121", "306619536!Moltkeplatz!52.392658!9.746416", "306621528!Weißekreuzplatz!52.380943!9.744822", "306632182!Emmichplatz!52.377377!9.752855", "306633317!Braunschweiger Platz!52.370671!9.76158", "306634776!Ricklinger Stadtweg!52.353567!9.72209", "306636890!Goetheplatz!52.373182!9.724649", "306637891!Celler Straße!52.382414!9.738634", "306638803!Herrenhäuser Markt!52.393611!9.683182", "306641629!Sallstraße!52.364814!9.756653", "306642669!Schaumburgstraße!52.392203!9.696132", "306644874!Leibnitz Universität/Schloßwender Straße!52.379871!9.723991", "306646326!Robert-Enke-Straße!52.362131!9.732363", "306647862!Lindener Marktplatz!52.366481!9.713958", "307167971!Steintor!52.376218!9.732354", "340929155!Alter Güterbahnhof!52.383634!9.732078", "349238105!Hauptbahnhof/ Rosenstraße!52.376893!9.738964", "491528970!Fenskestraße!52.396069!9.717911", "491529093!Podbielskistraße!52.405011!9.79768", "494484950!Stöcken Friedhof!52.400095!9.669964", "498525578!Zoo/Loebensteinstraße!52.381543!9.766315", "498527077!Hannover Congress Centrum!52.376968!9.768267", "501685208!Lister Damm!52.399205!9.754196", "501686803!Ricklinger Stadtweg!52.343127!9.72533", "502500548!Waterloo!52.368417!9.731183", "502644017!Faust!52.375553!9.71068", "503111106!BHF Leinhausen/Stöckener Staße!52.396907!9.674996", "503112749!Misburger Straße/ Berckhusenstraße!52.378684!9.807626", "503913022!Stresemannallee!52.358874!9.761186", "503913656!Stresemannallee!52.356837!9.762597", "504159382!Herschelstraße!52.38225!9.733195", "504161296!Hamburger Alle!52.383799!9.735678", "508767590!HerrenhäuserStr2!52.392468!9.686401", "508797016!Lange Laube!52.377007!9.726495", "510452084!Ritter-Brüning-Straße!52.354691!9.722096", "510661082!Universitätsbereich Schneiderberg!52.388088!9.712815", "510668681!Friesenstraße/Bödekerstraße!52.382135!9.753268", "510669510!Kantplatz!52.372216!9.785031", "510823763!Melanchthonstraße!52.397624!9.721034", "511030440!Brunnenstraße/Harenberger Straße!52.377364!9.68455", "511031589!Harenberger Straße!52.37703!9.68948", "511032542!Wunstorfer Straße!52.375422!9.69471", "511033558!HBF Süd 2!52.375727!9.741413", "511746900!Nordstadt BHF!52.392943!9.718856", "511748258!Kleefeld BHf!52.374063!9.790642", "511750351!Haltenhoffstraße!52.392871!9.714269", "512964246!HerrenhäuserStr1!52.391218!9.703277", "512979792!Fösse Straße!52.369488!9.702816", "513312395!Pier51!52.35436!9.746091", "513313081!Auf dem Emmerberge/Rudolf von Bennigsen Ufer!52.361528!9.740496", "513313802!NDR!52.359654!9.74189", "513369212!Alvenslebenstraße!52.398144!9.74174", "515857745!Stadionbrücke!52.358868!9.728254", "518186274!Wiehbergstraße!52.328734!9.776351", "518187588!Hildesheimer Straße / Peiner Straße!52.338086!9.768316", "518188627!Hildesheimer Straße / Flederstraße!52.34234!9.764646", "518189709!Klingerstraße / Podbialskistraße!52.402743!9.791517", "522790447!REWE / Wunstorfer Str!52.376418!9.693267", "524003076!Holzmarkt!52.371329!9.732567", "524251504!Nienburger Straße!52.382843!9.715583", "526095217!Hildesheimer Straße /Feldstraße!52.363448!9.74806", "535580393!Kalsruher Straße//Messe West!52.321596!9.795921", "549361281!Kötnerholzweg!52.372671!9.705713", "560798726!Messe Nord!52.327803!9.805201", "560799825!Messe Süd!52.319163!9.810405", "562880614!Weddigenufer!52.377446!9.716281", "562881229!Am Moritzwinkel!52.378229!9.71516", "562882007!Altenbekener Damm!52.355503!9.753923", "563250095!Hainholzer Markt!52.402111!9.71288", "563251452!Hannover Nordhafen!52.422013!9.689764", "563252736!Schulenburger Landstraße!52.419664!9.694737", "563255058!Schulenburger Landstraße 2!52.405276!9.712059", "563255677!Beneckeallee!52.414674!9.702693", "563917827!Wunstdorfer Straße/Conti!52.381048!9.680597", "563962959!Friedenauer Straße!52.412338!9.706115", "600959781!Rodenstraße/Fössestr!52.370041!9.705943", "606704630!Haltenhoffstraße SW!52.395018!9.704999", "606705162!Haltenhoffstraße GS!52.394347!9.707837", "607882729!Burgweg/Haltenhoffstraße!52.39581!9.701421", "607883109!Schützenplatz West!52.363726!9.724317", "607883401!Schützenplatz Süd!52.361233!9.727347", "610254646!MHH Ost!52.385832!9.808474", "611851824!Clausewitzstraße!52.375501!9.771609", "611900524!Nieschlagstraße!52.367123!9.708406", "612091846!Maschsee!52.363199!9.738752"};

        int i = 0;
        for (String station : stations) {
            String[] stationInfo = station.split("!");
            generateMarker(Integer.parseInt(stationInfo[0]), i, stationInfo[1], Double.parseDouble(stationInfo[2]), Double.parseDouble(stationInfo[3]));
            i += 1;
        }

        /*ViewCompat.setOnApplyWindowInsetsListener(binding.main, (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });*/


    }

    private void generateMarker(int id, int i, String name, double lat, double lon) {
        Marker marker = new Marker(mapView);
        GeoPoint stationPos = new GeoPoint(lat, lon);
        marker.setPosition(stationPos);
        marker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM);
        marker.setIcon(getDrawable(R.drawable.outline_directions_bike_24));
        mapView.getOverlays().add(marker);
        marker.setOnMarkerClickListener(new Marker.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(Marker marker, MapView mapView) {
                prepareRequest(i, id, name, stationPos);

                return true;
            }
        });

    }

    private void prepareRequest(int i, int id, String name, GeoPoint stationPos) {
        Request request = new Request.Builder()
                .url(""+String.valueOf(i+2))
                .build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                Log.e(TAG, "Request failed " + e.getMessage(), e);
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                try (Response res = response) {
                    if (!res.isSuccessful()) {
                        Log.e(TAG, "Unexpected code " + res);
                        return;
                    }
                    String body = res.body() != null ? res.body().string() : "";
                    Log.i(TAG, "Response " + body);
                    String numbers = body.replace("[", "").replace("]", "");
                    String[] s = numbers.split(",");
                    int [] data = {Integer.parseInt(String.valueOf(s[0])), Integer.parseInt(String.valueOf(s[1])), Integer.parseInt(String.valueOf(s[2])), Integer.parseInt(String.valueOf(s[3]))};
                    requestSuccesful(data, id, name, stationPos);
                }
            }
        });
    }

    private void requestSuccesful(int [] data, int id, String name, GeoPoint stationPos) {

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                showBottomDialog(name, id, data[0], data[1], data[2], data[3]);
                mapController.animateTo(stationPos);
            }
        });

    }

    private String getPrognoseSymbol(int current, int amountOne, int amountTwo, int amountThree) {
        double weightedSum = 0.5* amountOne + amountTwo + 1.5 * amountThree;
        double avg = weightedSum / 3;

        if (avg > 1.2*current) {
            return "+";
        } else if (avg < 0.8*current) {
            return "-";
        } else {
            return "~";
        }
    }


    private void showBottomDialog(String name, int id, int current, int amountOne, int amountTwo, int amountThree) {

        final Dialog dialog = new Dialog(this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.bottomsheet_layout);


        ImageView cancelButton = dialog.findViewById(R.id.cancelButton);

        TextView stationTitleText = dialog.findViewById(R.id.stationTitle);
        TextView currentAmountText = dialog.findViewById(R.id.currentAmount);
        TextView prognoseSymbolText = dialog.findViewById(R.id.trend);

        TextView trendNowText = dialog.findViewById(R.id.trendNow);
        TextView trendOneText = dialog.findViewById(R.id.trend_one);
        TextView trendTwoText = dialog.findViewById(R.id.trend_two);
        TextView trendThreeText = dialog.findViewById(R.id.trend_three);

        TextView percentageOneText = dialog.findViewById(R.id.percentage_one);
        TextView percentageTwoText = dialog.findViewById(R.id.percentage_two);
        TextView percentageThreeText = dialog.findViewById(R.id.percentage_three);

        stationTitleText.setText(name);

        currentAmountText.setText(String.valueOf(current));
        prognoseSymbolText.setText(getPrognoseSymbol(current, amountOne, amountTwo, amountThree));

        trendNowText.setText(String.valueOf(current));

        trendOneText.setText(String.valueOf(amountOne));
        trendTwoText.setText(String.valueOf(amountTwo));
        trendThreeText.setText(String.valueOf(amountThree));

        percentageOneText.setText("98%");
        percentageTwoText.setText("98%");
        percentageThreeText.setText("98%");


        cancelButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dialog.dismiss();
            }
        });

        dialog.show();
        dialog.getWindow().setLayout(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);

        dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        dialog.getWindow().getAttributes().windowAnimations = R.style.DialogAnimation;
        dialog.getWindow().setGravity(Gravity.BOTTOM);
    }




    @Override
    protected void onResume() {
        super.onResume();
        mapView.onResume();
    }
    @Override
    protected void onPause() {
        super.onPause();
        mapView.onPause();
    }
}