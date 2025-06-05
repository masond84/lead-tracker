import { DataTable } from "./DataTable";
import { type ColumnDef } from "@tanstack/react-table";

interface Props {
  results: any[];
}

export default function ResultTable({ results }: Props) {
  if (!results || results.length === 0) return null;

  const columns: ColumnDef<any>[] = Object.keys(results[0]).map((key) => ({
    accessorKey: key,
    header: key,
  }))

  return (
    <div className="w-full flex justify-center mt-6">
      <div className="w-full max-w-7xl px-4">
        <DataTable data={results} columns={columns} />
      </div>
    </div>
  )
}
