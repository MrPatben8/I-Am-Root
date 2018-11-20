using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Crosstales.FB;
using System.IO;

public class JsonReader : MonoBehaviour {
	public static JsonReader ins; void Awake() { ins = this; }
	#region Object
	[System.Serializable]
	public class Meteo
	{
		public bool nieve;
		public int nubes;
		public string precipitacion;
		public int intprecipitation;
	}
	[System.Serializable]
	public class Temp
	{
		public double evaporacion;
		public string maxx;
		public string minn;
		public int intmaxx;
		public int intminn;
		public int avrg;
	}
	[System.Serializable]
	public class Fecha
	{
		public string dia;
		public string mes;
		public Meteo meteo;
		public object numDia;
		public Temp temp;
	}
	[System.Serializable]
	public class LugaresJson
	{
		public List<Fecha> fecha;
		public double lat;
		public double @long;
		public string nombre;
	}
	[System.Serializable]
	public class RootObject
	{
		public List<LugaresJson> lugaresJson;
		public float duracionDia;
		public float velocidadAgua;
		public float velocidadCrecimiento;
		public float velocidadEvaporacion;
		public float velocidadMuerte;
	}
	#endregion
	public RootObject database;
	public Plant plant;

	// Use this for initialization
	void Start () {
		string extension = "json";
		string path = FileBrowser.OpenSingleFile("Seleccione base de dato:", "", extension);
		if(!File.Exists(path))
		{
			Start();
			return;
		}
		string jsonstring = File.ReadAllText(path);
		JsonUtility.FromJsonOverwrite(jsonstring, database);
		Parse();
		plant.database = database;
		plant.Begin();
	}

	void Parse()
	{
		foreach(LugaresJson lugar in database.lugaresJson)
		{
			foreach(Fecha fecha in lugar.fecha)
			{
				fecha.temp.intmaxx = int.Parse(fecha.temp.maxx);
				fecha.temp.intminn = int.Parse(fecha.temp.minn);
				fecha.meteo.intprecipitation = int.Parse(fecha.meteo.precipitacion);
				fecha.temp.avrg = Random.Range(fecha.temp.intminn, fecha.temp.intmaxx);
			}
		}
	}
}
