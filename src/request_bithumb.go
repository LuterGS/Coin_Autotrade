package src

import "encoding/json"

type publicOrder string
type privateOrder string

type BithumbRequester struct {
	requester *httpRequester

	basicUrl string

	ticker       publicOrder
	orderbook    publicOrder
	trHistory    publicOrder
	assetsStatus publicOrder
	btci         publicOrder
	candlestick  publicOrder

	balance privateOrder
}

func NewBithumbRequester(connectKey string, secretKey string) *BithumbRequester {

	bithumbRequester := BithumbRequester{}

	bithumbRequester.requester = newHttpRequester(connectKey, secretKey)

	// init public API address
	bithumbRequester.ticker = "/public/ticker"
	bithumbRequester.orderbook = "/public/orderbook"
	bithumbRequester.trHistory = "/public/transaction_history"
	bithumbRequester.assetsStatus = "/public/assetsstatus"
	bithumbRequester.btci = "/public/btci"
	bithumbRequester.candlestick = "/public/candlestick"

	// init private API address
	bithumbRequester.balance = "/private/balance"

	return &bithumbRequester
}

func (b *BithumbRequester) GetTicker(orderCurrency currency, paymentCurrency currency) Ticker {
	body := string(orderCurrency) + "_" + string(paymentCurrency)
	requestResult := b.requester.requestPublic(b.ticker, body)
	var result Ticker
	err := json.Unmarshal(requestResult, &result)
	if err != nil {
		panic(err)
	}
	if result.Status != 0 {
		Timelog("GetTicker Failed : ", result.Message)
	}
	return result
}

func (b *BithumbRequester) GetOrderbook(orderCurrency currency, paymentCurrency currency) Orderbook {
	body := string(orderCurrency) + "_" + string(paymentCurrency)
	requestResult := b.requester.requestPublic(b.orderbook, body)
	var result Orderbook
	err := json.Unmarshal(requestResult, &result)
	if err != nil {
		panic(err)
	}
	if result.Status != 0 {
		Timelog("GetOrderbook Failed : ", result.Message)
	}
	return result
}

func (b *BithumbRequester) GetTransactionHistory(orderCurrency currency, paymentCurrency currency) TransactionHistory {
	body := string(orderCurrency) + "_" + string(paymentCurrency)
	requestResult := b.requester.requestPublic(b.trHistory, body)
	var result TransactionHistory
	err := json.Unmarshal(requestResult, &result)
	if err != nil {
		panic(err)
	}
	if result.Status != 0 {
		Timelog("GetTransactionHistory Failed : ", result.Message)
	}
	return result
}

func (b *BithumbRequester) GetAssetsStatus(orderCurrency currency) AssetsStatus {
	body := string(orderCurrency)
	requestResult := b.requester.requestPublic(b.assetsStatus, body)
	var result AssetsStatus
	err := json.Unmarshal(requestResult, &result)
	if err != nil {
		panic(err)
	}
	if result.Status != 0 {
		Timelog("GetAssetsStatus Failed : ", result.Message)
	}
	return result
}

func (b *BithumbRequester) GetBTCI() BTCI {
	requestResult := b.requester.requestPublic(b.btci, "")
	var result BTCI
	err := json.Unmarshal(requestResult, &result)
	if err != nil {
		panic(err)
	}
	if result.Status != 0 {
		Timelog("GetBTCI Failed : ", result.Message)
	}
	return result
}

func (b *BithumbRequester) GetCandleStick(orderCurreny currency, paymentCurrency currency, chartInterval timeInterval) CandleStick {
	body := string(orderCurreny) + "_" + string(paymentCurrency) + "/" + string(chartInterval)
	requestResult := b.requester.requestPublic(b.candlestick, body)
	Timelog(string(requestResult))
	var rawResult RawCandleStick
	err := json.Unmarshal(requestResult, &rawResult)
	if rawResult.Status != 0 {
		Timelog("GetCandleStick Failed : ", rawResult.Message)
	}
	if err != nil {
		panic(err)
	}
	return NewCandleStick(rawResult)
}

func Test() {

	test := NewBithumbRequester("57bc35837f7f00c6f64a25d25ef69f6f", "7539214f665dfbd945dac04010b16eea")
	//Timelog(test.GetAssetsStatus(BTC))
	val := test.GetCandleStick(BTC, KRW, H24)
	Timelog(val)
	//Timelog(tval)

}
