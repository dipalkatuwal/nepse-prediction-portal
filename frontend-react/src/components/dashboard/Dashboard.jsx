import React, {useEffect} from 'react'
import axios from 'axios'
import axiosInstance from '../../axiosinstance'


const Dashboard = () => {
  

  useEffect(()=>{

  
  const fetchProctectedData =  async () =>{
    try{
      const response = await axiosInstance.get('/protected-view')
      console.log('Success:', response.data)
    }
    catch(error){
      console.error('Error fetching data:', error)
    }
  }
  fetchProctectedData();
  },[])
  return (
    <div className='text-light container'>Dashboard</div>
  )
}
export default Dashboard