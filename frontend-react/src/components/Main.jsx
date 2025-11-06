import Button from './Button'

const Main = () => {
  return (
    <>
    
    <div className='container'>
    <div className='p-5 text-center bg-light-dark rounded'>
      <h1 className='text-light'>Nepse Prediction Portal</h1>
      <p className='text-light lead'>This stock prediction apllication is blah blah</p>
      <Button text = 'Explore Now' class = "btn-info" url ="/dashboard"/>
    </div>

    </div>
    
    </>
  )

}
export default Main



