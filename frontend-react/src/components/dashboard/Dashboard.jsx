import React, { useEffect, useState } from 'react'
import axiosInstance from '../../axiosinstance'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'

const Dashboard = () => {
  const [ticker, setTicker] = useState('')
  const [loading, setLoading] = useState(false)
  const [plot, setPlot] = useState()
  const [ma100,setMA100] = useState()
  const [ma200,setMA200] = useState()
  const [prediction,setPrediction] = useState()
  const [mse,setMSE] = useState()
  const [rmse,setRMSE] = useState()
  const [r2,setR2] = useState()
  const [predictedPrice, setPredictedPrice] = useState()
  const [yesterdayPrice, setYesterdayPrice] = useState()
  const [nextweek,setNextWeek] = useState()

  
  // List of tickers
  const tickers = ["ADBL","AHPC","AKJCL","AKPL","ALICL","API","BARUN","BFC","BPCL","CBL","CCBL",
    "CFCL","CGH","CHCL","CHDC","CHL","CIT","CORBL","CZBIL","DHPL","EBL","EDBL","GBBL","GBIME","GFCL",
    "GHL","GLH","GMFIL","GRDBL","GUFL","HBL","HDHPC","HIDCL","HPPL","HURJA","ICFC","JBBL","JFL",
    "JOSHI","KBL","KKHC","KPCL","KSBBL","LBBL","LEC","LICN","MBL","MDB","MEN","MFIL","MHNL","MKJC",
    "MLBL","MNBBL","MPFL","NABBC","NABIL","NBL","NFS","NGPL","NHDL","NHPC","NICA","NIFRA","NLIC","NLICL",
    "NMB","NRN","NYADI","OHL","PCBL","PFL","PMHPL","PPCL","PROFL","PRVU","RADHI","RHPL","RLFL","RURU","SADBL",
    "SAHAS","SANIMA","SAPDBL","SBI","SBL","SCB","SFCL","SHEL","SHINE","SHL","SHPC","SIFC","SINDU","SJCL",
    "SPC","SPDL","SSHL","TPC","TRH","UMHL","UMRH","UNHPL","UPCL","UPPER"];

  useEffect(() => {
    const fetchProtectedData = async () => {
      try {
        const response = await axiosInstance.get('/protected-view')

      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }
    fetchProtectedData()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await axiosInstance.post('/predict/', { ticker })
      console.log(response.data)
      const backendRoot = import.meta.env.VITE_BACKEND_ROOT
      const plotUrl = `${backendRoot}${response.data.plot_img}`
      const ma100Url = `${backendRoot}${response.data.plot_100_dma}`
      const ma200Url = `${backendRoot}${response.data.plot_200_dma}`
      const prediction = `${backendRoot}${response.data.plot_prediction}`
      const nextweekUrl = `${backendRoot}${response.data.plot_next_week}`
      console.log(nextweekUrl)
      

      setPlot(plotUrl)
      setMA100(ma100Url)
      setMA200(ma200Url)
      setPrediction(prediction)
      setMSE(response.data.mse)
      setRMSE(response.data.rmse)
      setR2(response.data.r2)
      setPredictedPrice(response.data.predicted_price)
      setYesterdayPrice(response.data.yesterday_price)
      setNextWeek(nextweekUrl)

      // set plots
    } catch (error) {
      console.error('There was an error making the API request', error)
    }
    finally{
      setLoading(false);
    }
  }

  return (
    <div className='container mb-5'>
      <div className='row'>
        <div className='col-md-8 mx-auto'>
          <form onSubmit={handleSubmit}>
            <select
              className='form-control'
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              required
            >
              <option value=''>Select Stock Ticker</option>
              {tickers.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>

            <button type='submit' className='btn btn-info mt-3'>
              {loading ? <span><FontAwesomeIcon icon = {faSpinner} spin/>Please wait.....</span>:'See Prediction'}
            </button>
          </form>

              {/**print prediction plots */}
              {prediction && (
                <div className='prediction mt-5'>
                <div className='p-3'>
                  {plot && (
                    <img src={plot} style = {{maxWidth: '100%'}}/>
                  )}
                </div>
                <div className = 'p-3'>
                   {ma100 && (
                    <img src={ma100} style = {{maxWidth: '100%'}}/>
                  )}
                </div>
                <div className = 'p-3'>
                   {ma200 && (
                    <img src={ma200} style = {{maxWidth: '100%'}}/>
                  )}
                </div>
                <div className = 'p-3'>
                   {prediction && (
                    <img src={prediction} style = {{maxWidth: '100%'}}/>
                  )}
                </div>
                
                <div className='text-light p-3'>
                <h4>Model Evaluation</h4>
                <p>Mean Squared Error (MSE): {mse}</p>
                <p>Root Mean Squared Error (RMSE): {rmse}</p>
                <p>R-Squared: {r2}</p>
                < br />
                {yesterdayPrice && predictedPrice && (
                  <p>
                    Yesterday's Price: Rs. {yesterdayPrice.toFixed(2)} <br />
                    
                    Predicted Next Day Price: Rs. {predictedPrice.toFixed(2)}
                  </p>
                )}

              </div>
               <div className = 'p-3'>
                   {prediction && (
                    <img src={nextweek} style = {{maxWidth: '100%'}}/>
                  )}
                </div>
              </div>
              )}
              

        </div>
      </div>
    </div>
  )



  
}

export default Dashboard

