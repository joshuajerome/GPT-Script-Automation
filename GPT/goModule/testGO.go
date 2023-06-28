package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
)

var (
	confidentialFile = "confidential.json"
)

type ConfidentialData struct {
	IP   string `json:"IP"`
	USER string `json:"USER"`
	PASS string `json:"PASS"`
}

func main() {
	ip := flag.String("ip", "", "iDRAC IP address")
	u := flag.String("u", "", "iDRAC username")
	p := flag.String("p", "", "iDRAC password. If not provided, the script will prompt for the password without echoing it to the screen.")
	x := flag.String("x", "", "X-Auth session token for executing Redfish calls. All Redfish calls will use X-Auth token instead of username/password")
	scriptExamples := flag.Bool("script-examples", false, "Get executing script examples")

	flag.Parse()

	if *scriptExamples {
		printScriptExamples()
		os.Exit(0)
	}

	data := initialize()
	idracIP := data.IP
	idracUsername := data.USER
	idracPassword := data.PASS

	checkSupportedIDracVersion(ip, u, p, x, idracIP, idracUsername, idracPassword)
	getFirmwareInventory(ip, u, p, x, idracIP, idracUsername, idracPassword, false)
}

func initialize() ConfidentialData {
	file, err := os.Open(confidentialFile)
	if err != nil {
		log.Fatal("Failed to open confidential file:", err)
	}
	defer file.Close()

	var data ConfidentialData
	err = json.NewDecoder(file).Decode(&data)
	if err != nil {
		log.Fatal("Failed to decode confidential data:", err)
	}

	return data
}

func printScriptExamples() {
	fmt.Println("\n- GetFirmwareInventoryREDFISH.py -ip 100.100.0.100 -u username -p password, this example will return firmware inventory, current versions for all devices detected in the server.")
}

func checkSupportedIDracVersion(ip, u, p, x *string, idracIP, idracUsername, idracPassword string) {
	redfishAPIPath := fmt.Sprintf("https://%s/redfish/v1/Systems", *ip)

	var response *http.Response
	var err error

	if *x != "" {
		request, err := http.NewRequest("GET", redfishAPIPath, nil)
		if err != nil {
			log.Fatal("Failed to create HTTP request:", err)
		}
		request.Header.Set("X-Auth-Token", *x)

		client := &http.Client{}
		response, err = client.Do(request)
	} else {
		response, err = http.Get(redfishAPIPath)
	}
	if err != nil {
		log.Fatal("Failed to send the GET request:", err)
	}
	defer response.Body.Close()

	switch response.StatusCode {
	case 401:
		log.Printf("\n- WARNING, status code %d returned. Incorrect iDRAC username/password or invalid privilege detected.", response.StatusCode)
		os.Exit(0)
	case 200:
		// Successfully checked supported iDRAC version
	default:
		log.Println("\n- WARNING, installed iDRAC version does not support this feature using the Redfish API.")
		os.Exit(0)
	}
}

func getFirmwareInventory(ip, u, p, x *string, idracIP, idracUsername, idracPassword string, verifyCert bool) {
	redfishAPIPath := fmt.Sprintf("https://%s/redfish/v1/UpdateService/FirmwareInventory?$expand=*($levels=1)", *ip)

	var response *http.Response
	var err error

	if *x != "" {
		request, err := http.NewRequest("GET", redfishAPIPath, nil)
		if err != nil {
			log.Fatal("Failed to create HTTP request:", err)
		}
		request.Header.Set("X-Auth-Token", *x)

		client := &http.Client{}
		response, err = client.Do(request)
	} else {
		response, err = http.Get(redfishAPIPath)
	}
	if err != nil {
		log.Fatal("Failed to send the GET request:", err)
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		log.Printf("\n- ERROR, failed to get firmware inventory. Status code: %d", response.StatusCode)
		os.Exit(1)
	}

}
