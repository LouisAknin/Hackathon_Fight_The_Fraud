import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { mockClients } from "@/data/mockData";
import { RiskBadge } from "@/components/RiskBadge";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";

export default function Clients() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");

  const filteredClients = mockClients.filter((client) =>
    client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Clients</h1>
        <p className="text-muted-foreground">Gérez votre portefeuille clients</p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher un client..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-medium">Client</th>
                  <th className="text-left py-3 px-4 font-medium">Contact</th>
                  <th className="text-left py-3 px-4 font-medium">Agence</th>
                  <th className="text-right py-3 px-4 font-medium">Actifs</th>
                  <th className="text-center py-3 px-4 font-medium">Risque</th>
                </tr>
              </thead>
              <tbody>
                {filteredClients.map((client) => (
                  <tr
                    key={client.id}
                    onClick={() => navigate(`/client/${client.id}`)}
                    className="border-b border-border hover:bg-accent cursor-pointer transition-colors"
                  >
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                          <span className="font-medium text-primary">
                            {client.name.split(" ").map((n) => n[0]).join("")}
                          </span>
                        </div>
                        <div>
                          <p className="font-medium">{client.name}</p>
                          <p className="text-sm text-muted-foreground">{client.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <p className="text-sm">{client.email}</p>
                      <p className="text-sm text-muted-foreground">{client.phone}</p>
                    </td>
                    <td className="py-3 px-4 text-muted-foreground">{client.branch}</td>
                    <td className="py-3 px-4 text-right font-medium">
                      {client.totalAssets.toLocaleString("fr-FR")}€
                    </td>
                    <td className="py-3 px-4 text-center">
                      <RiskBadge score={client.riskScore} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
