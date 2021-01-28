package src

type currency string
type timeInterval string

const (
	BTC currency = "btc"
	KRW currency = "krw"
	ETH currency = "eth"
	ALL currency = "all" // -> 어떻게 짤 것인지 생각해봐야 함

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
