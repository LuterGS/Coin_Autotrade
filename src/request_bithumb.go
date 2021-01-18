package src

type BithumbRequester struct {
	connectKey string
	secretKey  string
}

func (b *BithumbRequester) NewBithumbRequester() *BithumbRequester {

	bithumbRequester := BithumbRequester{}

	getFileVal := readFromFile("/setting/" + KEY_FILE)
	bithumbRequester.connectKey = getFileVal["connect_key"]
	bithumbRequester.secretKey = getFileVal["secret_key"]

	return &bithumbRequester
}
