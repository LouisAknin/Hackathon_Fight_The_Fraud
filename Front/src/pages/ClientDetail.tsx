import { useParams, useNavigate } from "react-router-dom";
import { mockClients, mockAccounts, mockTransactions, mockFraudData } from "@/data/mockData";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { RiskBadge } from "@/components/RiskBadge";
import { ArrowLeft, Mail, Phone, MapPin, Shield, CheckCircle, AlertTriangle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function ClientDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const client = mockClients.find((c) => c.id === id);
  const accounts = mockAccounts.filter((a) => a.clientId === id);
  const transactions = mockTransactions.filter((t) => t.clientId === id);
  const fraudData = mockFraudData.filter((f) => f.clientId === id);

  if (!client) {
    return <div>Client non trouvé</div>;
  }

  const chartData = accounts.map((acc) => ({
    name: acc.type,
    balance: acc.balance,
  }));

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <Button
        variant="ghost"
        onClick={() => navigate("/clients")}
        className="gap-2"
      >
        <ArrowLeft className="h-4 w-4" />
        Retour aux clients
      </Button>

      {/* Client Header */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-6 items-start">
            <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center">
              <span className="font-bold text-primary text-2xl">
                {client.name.split(" ").map((n) => n[0]).join("")}
              </span>
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h1 className="text-3xl font-bold">{client.name}</h1>
                <p className="text-muted-foreground">Client ID: {client.id}</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="flex items-center gap-2 text-sm">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span>{client.email}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span>{client.phone}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span>{client.branch}</span>
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-2 items-end">
              <RiskBadge score={client.riskScore} />
              <p className="text-2xl font-bold">
                {client.totalAssets.toLocaleString("fr-FR")}€
              </p>
              <p className="text-sm text-muted-foreground">Total actifs</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="bg-muted">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="accounts">Comptes</TabsTrigger>
          <TabsTrigger value="transactions">Transactions</TabsTrigger>
          <TabsTrigger value="fraud">
            <Shield className="h-4 w-4 mr-2" />
            Détection Fraude
            {fraudData.length > 0 && (
              <span className="ml-2 bg-destructive text-destructive-foreground rounded-full px-2 py-0.5 text-xs">
                {fraudData.length}
              </span>
            )}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Répartition des Comptes</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="balance" fill="hsl(var(--primary))" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Informations Client</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground">Nombre de comptes</p>
                  <p className="text-2xl font-bold">{accounts.length}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Agence</p>
                  <p className="font-medium">{client.branch}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Score de risque</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary"
                        style={{ width: `${client.riskScore * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium">
                      {(client.riskScore * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="accounts">
          <Card>
            <CardHeader>
              <CardTitle>Comptes du Client</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {accounts.map((account) => (
                  <div
                    key={account.id}
                    className="p-4 border border-border rounded-lg hover:bg-accent transition-colors"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold">{account.productName}</h3>
                        <p className="text-sm text-muted-foreground">{account.type}</p>
                        <p className="text-xs text-muted-foreground mt-1">{account.accountNumber}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold">
                          {account.balance.toLocaleString("fr-FR")}€
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="transactions">
          <Card>
            <CardHeader>
              <CardTitle>Transactions Récentes</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left py-3 px-4 font-medium">Date</th>
                      <th className="text-left py-3 px-4 font-medium">Type</th>
                      <th className="text-left py-3 px-4 font-medium">Description</th>
                      <th className="text-right py-3 px-4 font-medium">Montant</th>
                      <th className="text-center py-3 px-4 font-medium">Statut</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.map((transaction) => (
                      <tr key={transaction.id} className="border-b border-border">
                        <td className="py-3 px-4 text-sm">{transaction.date}</td>
                        <td className="py-3 px-4 text-sm">{transaction.type}</td>
                        <td className="py-3 px-4 text-sm">{transaction.merchant}</td>
                        <td className={`py-3 px-4 text-right font-medium ${
                          transaction.amount > 0 ? "text-success" : ""
                        }`}>
                          {transaction.amount > 0 ? "+" : ""}
                          {transaction.amount.toLocaleString("fr-FR")}€
                        </td>
                        <td className="py-3 px-4 text-center">
                          <span className="px-2 py-1 bg-success/10 text-success rounded-full text-xs">
                            {transaction.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="fraud" className="space-y-4">
          {fraudData.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <CheckCircle className="h-12 w-12 text-success mb-4" />
                <h3 className="text-lg font-semibold">Aucune alerte fraude</h3>
                <p className="text-muted-foreground">Ce client ne présente aucune activité suspecte</p>
              </CardContent>
            </Card>
          ) : (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5 text-destructive" />
                    Score de Fraude Global
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-4">
                    <div className="flex-1">
                      <div className="h-4 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-destructive transition-all"
                          style={{ width: `${client.riskScore * 100}%` }}
                        />
                      </div>
                    </div>
                    <RiskBadge score={client.riskScore} />
                  </div>
                  <p className="text-sm text-muted-foreground mt-2">
                    {fraudData.filter((f) => !f.reviewed).length} message(s) non traité(s)
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Messages Suspects Détectés</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {fraudData.map((fraud) => (
                      <div
                        key={fraud.id}
                        className={`p-4 border rounded-lg ${
                          fraud.reviewed ? "border-border bg-muted/50" : "border-destructive/50 bg-destructive/5"
                        }`}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div className="flex items-center gap-2">
                            <RiskBadge score={fraud.score} />
                            <span className="text-sm text-muted-foreground">{fraud.date}</span>
                          </div>
                          {fraud.reviewed && (
                            <span className="px-2 py-1 bg-success/10 text-success rounded-full text-xs">
                              Traité
                            </span>
                          )}
                        </div>
                        <div className="space-y-2">
                          <div>
                            <p className="text-sm font-medium">Numéro: {fraud.scammerNumber}</p>
                          </div>
                          <div className="p-3 bg-background rounded border border-border">
                            <p className="text-sm">{fraud.messageText}</p>
                          </div>
                          <div className="flex items-start gap-2 p-2 bg-warning/10 rounded">
                            <AlertTriangle className="h-4 w-4 text-warning mt-0.5" />
                            <p className="text-sm text-warning-foreground">{fraud.analysis}</p>
                          </div>
                        </div>
                        {!fraud.reviewed && (
                          <div className="flex gap-2 mt-3">
                            <Button size="sm" variant="outline">
                              Marquer comme traité
                            </Button>
                            <Button size="sm" variant="destructive">
                              Escalader
                            </Button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
