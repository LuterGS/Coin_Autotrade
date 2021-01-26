package src

type currency string
type timeInterval string

const (
	BTC currency = "btc"
	KRW currency = "krw"

	M1  timeInterval = "1m"
	M3  timeInterval = "3m"
	M5  timeInterval = "5m"
	M10 timeInterval = "10m"
	M30 timeInterval = "30m"
	H1  timeInterval = "1h"
	H6  timeInterval = "6h"
	H12 timeInterval = "12h"
	H24 timeInterval = "24h"
)
