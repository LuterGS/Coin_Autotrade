package src

import (
	"strconv"
	"time"
)

//=============== RAW GETTER ==================

type RawTicker struct {
	Status int `json:"status,string"`

	Data struct {
		coin []interface{}
	} `json:"data"`
}

type AllTicker struct {
	Status int
	Data   map[string]interface{}
}

type Ticker struct {
	Status  int    `json:"status,string"`
	Message string `json:"message"`
	Data    struct {
		OpeningPrice     int     `json:"opening_price,string"`
		ClosingPrice     int     `json:"closing_price,string"`
		MinPrice         int     `json:"min_price,string"`
		MaxPrice         int     `json:"max_price,string"`
		UnitsTraded      float64 `json:"units_traded,string"`
		AccTradeValue    float64 `json:"acc_trade_value,string"`
		PrevClosingPrice float64 `json:"prev_closing_price,string"`
		UnitsTraded24H   float64 `json:"units_traded_24H,string"`
		AccTradeValue24H float64 `json:"acc_trade_value_24H,string"`
		Fluctate24H      int     `json:"fluctate_24H,string"`
		FluctateRate24H  float64 `json:"fluctate_rate_24H,string"`
		Date             string  `json:"date"`
	} `json:"data"`
}

type Orderbook struct {
	Status  int    `json:"status,string"`
	Message string `json:"message"`
	Data    struct {
		Timestamp       string `json:"timestamp"`
		PaymentCurrency string `json:"payment_currency"`
		OrderCurrency   string `json:"order_currency"`
		Bids            []struct {
			Price    int     `json:"price,string"`
			Quantity float64 `json:"quantity,string"`
		} `json:"bids"`
		Asks []struct {
			Price    int     `json:"price,string"`
			Quantity float64 `json:"quantity,string"`
		} `json:"asks"`
	} `json:"data"`
}

type TransactionHistory struct {
	Status  int    `json:"status,string"`
	Message string `json:"message"`
	Data    []struct {
		TransactionDate string  `json:"transaction_date"`
		Type            string  `json:"type"`
		UnitsTraded     float64 `json:"units_traded,string"`
		Price           int     `json:"price,string"`
		Total           int     `json:"total,string"`
	}
}

type AssetsStatus struct {
	Status  int    `json:"status,string"`
	Message string `json:"message"`
	Data    struct {
		WithdrawlStatus int `json:"withdrawl_status"`
		DepositStatus   int `json:"deposit_status"`
	}
}

type BTCI struct {
	Status  int    `json:"status,string"`
	Message string `json:"message"`
	Data    struct {
		Btai struct {
			MarketIndex float64 `json:"market_index,string"`
			Width       float64 `json:"width,string"`
			Rate        float64 `json:"rate,string"`
		}
		Btmi struct {
			MarketIndex float64 `json:"market_index,string"`
			Width       float64 `json:"width,string"`
			Rate        float64 `json:"rate,string"`
		}
		Date string `json:"date"`
	}
}

type RawCandleStick struct {
	Status  int    `json:"status,string"`
	Message string `json:"message"`
	Data    [][]interface{}
}

type candleStickData struct {
	Time         time.Time
	OpeningPrice int
	ClosingPrice int
	HighPrice    int
	LowPrice     int
	UnitsTraded  float64
}

type CandleStick struct {
	Status int
	Data   []candleStickData
}

func NewCandleStick(rawCandleStick RawCandleStick) CandleStick {
	newCandleStick := CandleStick{}
	newCandleStick.Status = rawCandleStick.Status
	newCandleStick.Data = make([]candleStickData, len(rawCandleStick.Data))
	for index, data := range rawCandleStick.Data {
		newCandleStick.Data[index].Time = time.Unix(int64(data[0].(float64)/1000), 0)
		newCandleStick.Data[index].OpeningPrice, _ = strconv.Atoi(data[1].(string))
		newCandleStick.Data[index].ClosingPrice, _ = strconv.Atoi(data[2].(string))
		newCandleStick.Data[index].HighPrice, _ = strconv.Atoi(data[3].(string))
		newCandleStick.Data[index].LowPrice, _ = strconv.Atoi(data[4].(string))
		newCandleStick.Data[index].UnitsTraded, _ = strconv.ParseFloat(data[5].(string), 64)
	}
	return newCandleStick
}

//====================== Private API 관련 ========================

type RawBalance struct {
	Status int `json:"status,string"`
	Data   map[string]interface{}
}

type Balance struct {
	Status int
	Data   struct {
		TotalKrw        float64
		InUseKrw        float64
		AvailableKrw    float64
		TotalCrypto     float64
		InUseCrypto     float64
		AvailableCrypto float64
		XCoinLastCrypto float64
	}
}

func NewBalance(rawBalance RawBalance, coin currency) Balance {
	strCoin := string(coin)

	newBalance := Balance{}
	newBalance.Status = rawBalance.Status
	newBalance.Data.TotalKrw, _ = strconv.ParseFloat(rawBalance.Data["total_krw"].(string), 64)
	newBalance.Data.InUseKrw, _ = strconv.ParseFloat(rawBalance.Data["in_use_krw"].(string), 64)
	newBalance.Data.AvailableKrw, _ = strconv.ParseFloat(rawBalance.Data["available_krw"].(string), 64)
	newBalance.Data.TotalCrypto, _ = strconv.ParseFloat(rawBalance.Data["total_"+strCoin].(string), 64)
	newBalance.Data.InUseCrypto, _ = strconv.ParseFloat(rawBalance.Data["in_use_"+strCoin].(string), 64)
	newBalance.Data.AvailableCrypto, _ = strconv.ParseFloat(rawBalance.Data["available_"+strCoin].(string), 64)
	newBalance.Data.XCoinLastCrypto, _ = strconv.ParseFloat(rawBalance.Data["xcoin_last_"+strCoin].(string), 64)

	return newBalance
}
