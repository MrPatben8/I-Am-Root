using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Plant : MonoBehaviour {

    // Use this for initialization
    public SpriteRenderer sprite;
    public Sprite[] plantSprites;
    public float plantGrowth;

	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
        sprite.sprite = plantSprites[Mathf.Clamp(Mathf.FloorToInt(plantGrowth / plantSprites.Length),0,plantSprites.Length-1)];
	}
}
