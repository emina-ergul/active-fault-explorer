import { useState, useEffect } from "react";
import "leaflet/dist/leaflet.css";
import { Card } from "@/shadcnComponents/ui/card";
import { getFaultCount } from "../services/api";

type faultCount = {
  count: number;
};

function Menubar() {
    const [faultCount, setFaultCount] = useState<faultCount | null>(null);

    useEffect(() => {
        const fetchFaultCount = async () => {
            try {
                const data = await getFaultCount();
                setFaultCount(data);
            } catch (error) {
                console.error("Error fetching fault count:", error);
            }
        }
        fetchFaultCount();
    }, []);

    return (
        <div className="menubar-container">
            <h1>Seismic Explorer</h1>
            <div className="menubar-panels-container">
                <Card className="panel">
                    <h2>Earthquake count</h2>
                    <span>0</span>
                </Card>
                <Card className="panel">
                    <h2>Fault count</h2>
                    <span>{faultCount ? faultCount.count : ""}</span>
                </Card>
                <Card className="panel">
                    <h2>Time window</h2>
                    <span>Past 30 days</span>
                </Card>
            </div>
        </div>
    );
}

export default Menubar;
 