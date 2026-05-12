import Button from './Button'

const Main = () => {
  return (
    <div className="container mt-5">
      <div className="p-5 text-center rounded glass-card shadow-lg">
        <h1 className="text-light fw-bold mb-3">
          Nepse Prediction Portal
        </h1>

        <p className="text-light opacity-75 lead mb-4">
          Welcome to the NEPSE Prediction Portal — your intelligent companion for
          understanding Nepal’s stock market trends.
          <br />
          Powered by machine learning to analyze historical data and predict
          future movements.
        </p>

        <Button
          text="Explore"
          class="btn-info px-4 py-2 fw-semibold"
          url="/dashboard"
        />
      </div>
    </div>
  )
}

export default Main
