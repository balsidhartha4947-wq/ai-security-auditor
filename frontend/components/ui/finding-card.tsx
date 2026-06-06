import {
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from "@/components/ui/card"

import { Badge } from "@/components/ui/badge"

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger
} from "@/components/ui/accordion"

import { getSeverityColor } from "@/lib/severity"

export default function FindingCard({ item }: any) {

  const finding = item.finding

  return (
    <Card className="mb-4">

      <CardHeader>

        <div className="flex items-center justify-between">

          <CardTitle className="text-lg">
            {finding.message}
          </CardTitle>

          <Badge className={getSeverityColor(finding.severity)}>
            {finding.severity}
          </Badge>

        </div>

        <p className="text-sm text-muted-foreground">
          {finding.path}
        </p>

      </CardHeader>

      <CardContent>

        <Accordion type="single" collapsible>

          <AccordionItem value="details">

            <AccordionTrigger>
              AI Analysis
            </AccordionTrigger>

            <AccordionContent>

              <div className="whitespace-pre-wrap text-sm">
                {item.ai_analysis}
              </div>

            </AccordionContent>

          </AccordionItem>

        </Accordion>

      </CardContent>

    </Card>
  )
}