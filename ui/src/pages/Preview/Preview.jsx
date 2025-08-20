import { useState, useEffect } from "react";
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import PreviewChatBox from "./ChatBox"
import { getBotConfiguration, getBotConfigurationById } from "src/services/BotConfifuration";


const Preview = ()=>{ 
    const [select, setSelect] = useState(false);
    const [options, setOptions] = useState([]);
    const [selectedOption, setSelectedOption] = useState(null);
    const [connOptions, connSetOptions] = useState([]);
    const [connSelectedOption, connSetSelectedOption] = useState(null);

    

    const getConfig = ()=>{
            getBotConfiguration().then(response=>{
                let configs = response.data?.data?.configurations
                if(configs?.length > 0){
                    setSelect(true)
                    let configList = []
                    configs.map(item => {
                        configList.push({ value: item.id, label: item.name})
                    })
                    setOptions(configList);  
                    setSelectedOption(configList[0])
                }
            })
        }
    
    const getConnectors = (configId)=>{
        if (!configId) return;
        getBotConfigurationById(configId).then(response=>{
            let connectors = response.data?.data?.configuration?.connector
            if (connectors?.length > 0){
                let connectorList = []
                connectorList.push({ value: "", label: "Auto"})
                connectors.map(item => {
                    connectorList.push({ value: item.connector_name, label: item.connector_name})
                })
                connSetOptions(connectorList);
                connSetSelectedOption(connectorList[0])
            }
        })
    }
    
    useEffect(() => {
        getConfig(); 
    }, []);

    useEffect(() => {
        getConnectors(selectedOption?.value); 
    }, [selectedOption]);



    return(
        <DashboardBody title="Preview" options={options} select={select} selectedOption={selectedOption} setSelectedOption={setSelectedOption} connOptions={connOptions} connSelectedOption={connSelectedOption} connSetSelectedOption={connSetSelectedOption} containerStyle={{padding: "0px 0px", height: "calc(100vh - 76px)"}}>
            <PreviewChatBox selectedOption={selectedOption} setSelectedOption={setSelectedOption} connSelectedOption={connSelectedOption} connSetSelectedOption={connSetSelectedOption}/>
        </DashboardBody>
    )
}

export default Preview