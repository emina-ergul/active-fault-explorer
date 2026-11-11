import { useState } from "react";
import { Button } from "@/shadcnComponents/ui/button";
import { Switch } from "@/shadcnComponents/ui/switch";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface PanelProps {
  earthquakesOn: boolean;
  setEarthquakesOn: (value: boolean) => void;
  faultsOn: boolean;
  setFaultsOn: (value: boolean) => void;
}

function Panel({
  earthquakesOn,
  setEarthquakesOn,
  faultsOn,
  setFaultsOn,
}: PanelProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`filter-panel ${collapsed ? "collapsed" : ""}`}>
      <div className="panel-header">
        <h3 className="panel-heading">MAP LAYERS</h3>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          aria-label={collapsed ? "Expand panel" : "Collapse panel"}
        >
          <span className="chevron">
            {collapsed ? <ChevronRight /> : <ChevronLeft />}
          </span>
        </Button>
      </div>

      {!collapsed && (
        <div className="panel-section">
          <div className="layer-control">
            <span>Earthquakes</span>
            <Switch
              className="switch"
              checked={earthquakesOn}
              onCheckedChange={setEarthquakesOn}
            />
          </div>

          <div className="layer-control">
            <span>Active faults</span>
            <Switch
              className="switch"
              checked={faultsOn}
              onCheckedChange={setFaultsOn}
            />
          </div>
        </div>
      )}
    </aside>
  );
}

export default Panel;
