package src

import (
	"io/ioutil"
	"net/http"
	"time"
)

type httpRequester struct {
	connectKey string
	secretKey  string

	basicUrl string

	publicClient  *http.Client
	privateClient *http.Client
}

func newHttpRequester(connectKey string, secretKey string) *httpRequester {

	httpRequester := httpRequester{}

	httpRequester.connectKey = connectKey
	httpRequester.secretKey = secretKey
	httpRequester.basicUrl = "https://api.bithumb.com"

	httpRequester.publicClient = &http.Client{}
	httpRequester.privateClient = &http.Client{}

	return &httpRequester
}

func (h *httpRequester) requestPublic(order publicOrder, data string) []byte {

	Timelog(h.basicUrl + string(order) + "/" + data)

	request, err := http.NewRequest("GET", h.basicUrl+string(order)+"/"+data, nil)
	if err != nil {
		panic("Failed to create Request")
	}

	response, err := h.publicClient.Do(request)
	if err != nil {
		panic("Failed to receive Data, check server status")
	}

	byteResponse, err := ioutil.ReadAll(response.Body)
	if err != nil {
		panic("Failed to receive Data")
	}
	return byteResponse
}

func (h *httpRequester) requestPrivate() {

	Timelog(time.Now())
}
