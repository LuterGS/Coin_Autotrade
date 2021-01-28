package src

import (
	"strconv"
	"time"
)

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

type GetBalance struct {
	Currency string `json:"currency"`
	Endpoint string `json:"endpoint"`
}
