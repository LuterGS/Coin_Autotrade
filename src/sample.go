package src

type TEST struct {
	Container []byte
}

func (t *TEST) Write(writer []byte) (int, error) {

	t.Container = writer

	return len(writer), nil
}
