using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Plant : MonoBehaviour {
	public static Plant ins; void Awake() { ins = this; }
	// Use this for initialization
	public GameObject map;
	public Transform[] zoom;
	public int zoomNum = 1;

    public Image sprite;
    public Sprite[] plantSprites;

	public float evaporationMultiplier = 1;
	public float wetMultiplier = 10;
	public float growthMultiplier = 1;
	public float dryMultiplier = 1;
    public float plantGrowth;
	public float plantWater = 100;
	public int plantIdealTemp = 25;

	public JsonReader reader;
	public JsonReader.RootObject database;

	public Text calendar;
	public ParticleSystem rain;
	public ParticleSystem clouds;

	#region Day Config
	int day = 0;
	public float dayDuration = 1.2f;
	#endregion

	public JsonReader.Fecha selectedPlaceStat;

	public GameObject placeMarker;
	[System.Serializable]
	public class Place
	{
		public string name;
		public bool selected;
		public int index;
		public GameObject pointer;
		public GameObject marker;
		public SpriteRenderer miniWeather;
		public TextMesh temp;
		public TextMesh temp2;
		public TextMesh nameMesh;
		public int zoolLvl;
	}

	public List<Place> places;

	public GameObject[] pointers;

	[System.Serializable]
	public class MiniWeather
	{
		public Sprite icon;
		public int minClouds;
		public int minRain;
	}
	public MiniWeather[] miniWeathers;
	public Gradient tempColorGradient;
	public Material rainMat;
	public Texture rainTexture;
	public Texture snowTexture;

	public Slider water;
	public Text dayTemp;
	public Text nameDisplay;
	int selectedplace = 4;

	public GameObject endScreen;
	public Text scoreText;
	public Text maxGrowthText;
	public int maxGrowth;

	public void Begin() {
		day = 0;
		LoadPlaces();
		Select("Santiago");
		dayDuration = database.duracionDia;
		wetMultiplier = database.velocidadAgua;
		growthMultiplier = database.velocidadCrecimiento;
		evaporationMultiplier = database.velocidadEvaporacion;
		dryMultiplier = database.velocidadMuerte;
		endScreen.SetActive(false);
	}
	
	public void Select(string name)
	{
		int x = 0;
		foreach(Place pl in places)
		{
			if(pl.name == name)
			{
				pl.selected = true;
				selectedplace = x;
				zoomNum = pl.zoolLvl;
				nameDisplay.text = pl.name;
			} else
			{
				pl.selected = false;
			}
			x++;
		}
	}

	void LoadPlaces()
	{
		GetMinMax();
		int idx = 0;
		foreach(JsonReader.LugaresJson jsonplace in database.lugaresJson)
		{
			Place newPlace = new Place();
			newPlace.name = jsonplace.nombre;
			foreach(GameObject point in pointers)
			{
				if(jsonplace.nombre == point.name)
				{
					newPlace.pointer = point;
					newPlace.marker = (GameObject)Instantiate(placeMarker, newPlace.pointer.transform.position, Quaternion.identity, newPlace.pointer.transform);
					newPlace.nameMesh = newPlace.marker.transform.Find("name").GetComponent<TextMesh>();
					newPlace.temp = newPlace.marker.transform.Find("temp").GetComponent<TextMesh>();
					newPlace.temp2 = newPlace.marker.transform.Find("temp2").GetComponent<TextMesh>();
					newPlace.miniWeather = newPlace.marker.transform.Find("mini").GetComponent<SpriteRenderer>();
					newPlace.nameMesh.text = newPlace.name;
					newPlace.zoolLvl = 1;
					if(jsonplace.lat < -40)
						newPlace.zoolLvl = 2;
					if(jsonplace.lat > -30)
						newPlace.zoolLvl = 0;
				}
			}
			newPlace.index = idx;
			places.Add(newPlace);
			idx++;
		}
		places[4].selected = true;
	}


	void GrowPlant()
	{
		if(plantWater > 0)
		{
			plantGrowth += growthMultiplier * selectedPlaceStat.temp.avrg;
		} else {
			plantGrowth -= dryMultiplier;
		}
		plantWater -= evaporationMultiplier * (float)selectedPlaceStat.temp.evaporacion;
		plantWater += wetMultiplier * selectedPlaceStat.meteo.intprecipitation;
		plantWater = Mathf.Clamp(plantWater, 0, 100);
		plantGrowth = Mathf.Clamp(plantGrowth, 0, Mathf.Infinity);
		water.value = plantWater / 100.0f;
		dayTemp.text = "" + selectedPlaceStat.temp.avrg + "°";
		if(plantGrowth > maxGrowth)
		{
			maxGrowth = (int)plantGrowth;
		}
	}

	private void Update()
	{
		if(Input.anyKeyDown)
		{
			int cng = (int)Input.GetAxis("Vertical");
			selectedplace -= cng;
			selectedplace = Mathf.Clamp(selectedplace, 0, places.Count - 1);
			if(cng != 0)
				Select(places[selectedplace].name);
		}
	}

	public void Restart()
	{
		Application.LoadLevel(0);
	}

	float lastDayTime = 0;
	// Update is called once per frame
	void FixedUpdate () {
		map.transform.position = zoom[zoomNum].position;
		if(day > 365)
		{
			endScreen.SetActive(true);
			scoreText.text = "Final Score: " + (int)plantGrowth;
			maxGrowthText.text = "Maximum Score: " + maxGrowth;
			return;
		}

		if(Time.time - lastDayTime > dayDuration)
		{
			day++;
			lastDayTime = Time.time;
		}
        sprite.sprite = plantSprites[Mathf.Clamp(Mathf.FloorToInt(plantGrowth / plantSprites.Length),0,plantSprites.Length-1)];
		calendar.text = "" + database.lugaresJson[0].fecha[day].dia + "/" + database.lugaresJson[0].fecha[day].mes;
		foreach(Place pl in places)
		{
			if(pl.selected)
			{
				selectedPlaceStat = database.lugaresJson[pl.index].fecha[day];
			}
		}
		var em = rain.emission;
		em.enabled = true;
		em.rateOverTime = new ParticleSystem.MinMaxCurve(10 * selectedPlaceStat.meteo.intprecipitation);
		var clr = rain.colorOverLifetime;
		var main = rain.main;
		if(selectedPlaceStat.meteo.nieve)
		{
			clr.color = Color.white;
			rainMat.mainTexture = snowTexture;
			main.gravityModifier = 0.1f;
			main.startSize = new ParticleSystem.MinMaxCurve(0.5f, 1.5f);

		} else
		{
			clr.color = Color.blue;
			rainMat.mainTexture = rainTexture;
			main.gravityModifier = 1;
			main.startSize = new ParticleSystem.MinMaxCurve(0.1f, 0.5f);
		}
		var clem = clouds.emission;
		clem.rateOverTime = selectedPlaceStat.meteo.nubes;
		foreach(Place pl in places)
		{
			pl.temp.text = "" + database.lugaresJson[pl.index].fecha[day].temp.intmaxx + "°";
			pl.temp2.text = "" + database.lugaresJson[pl.index].fecha[day].temp.intminn + "°";
			pl.miniWeather.sprite = GetIcon(pl);
			if(pl.selected)
			{
				pl.nameMesh.color = Color.green;
			} else
			{
				pl.nameMesh.color = Color.black;
			}
		}
		GrowPlant();
	}

	Sprite GetIcon(Place pl)
	{
		Sprite icn = null;
		JsonReader.Fecha temp = database.lugaresJson[pl.index].fecha[day];
		foreach(MiniWeather mini in miniWeathers)
		{
			if(temp.meteo.intprecipitation > 0)
			{
				if(mini.minRain >= temp.meteo.intprecipitation)
				{
					icn = mini.icon;
				}
			} else {
				if(mini.minClouds >= temp.meteo.nubes)
				{
					icn = mini.icon;
				}
			}
		}
		if(icn == null)
		{
			return miniWeathers[0].icon;
		}
		return icn;
	}

	void GetMinMax()
	{
		int minTemp = 99;
		int maxTemp = -99;
		int maxPreci = 0;
		foreach(JsonReader.LugaresJson lugar in database.lugaresJson)
		{
			foreach(JsonReader.Fecha fecha in lugar.fecha)
			{
				if(fecha.temp.intminn < minTemp)
					minTemp = fecha.temp.intminn;

				if(fecha.temp.intmaxx > maxTemp)
					maxTemp = fecha.temp.intmaxx;

				if(fecha.meteo.intprecipitation > maxPreci)
					maxPreci = fecha.meteo.intprecipitation;
			}
		}
		Debug.Log(minTemp);
		Debug.Log(maxTemp);
		Debug.Log(maxPreci);
	}
}
