import { FormEvent } from "react";

interface FormInputProps {
  form: "select" | "text" | "number";
  onChange: (e: FormEvent) => void;
  options: string[];
  label: string;
  value: string | number;
  placeholder: string;
}

export default function FormInput(props: FormInputProps) {
  const { form, onChange, options, label, value, placeholder } = props;
  if (form == "select") {
    return (
      <div className="flex flex-col justify-between items-center">
        <label htmlFor="period">{label}</label>
        <select
          value={value}
          onChange={onChange}
          className="w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        >
          {options.map((choice) => (
            <option key={choice} value={choice}>
              {choice}
            </option>
          ))}
        </select>
      </div>
    );
  } else if (form == "text") {
    return (
      <div className="flex flex-col justify-between items-center">
        <label htmlFor="period">{label}</label>
        <input
          type="text"
          value={value}
          onChange={onChange}
          className="w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          placeholder={placeholder}
        />
      </div>
    );
  } else {
    return (
      <div className="flex flex-col justify-between items-center">
        <label htmlFor="initialCapital">{label}</label>
        <input
          type="number"
          value={value}
          onChange={onChange}
          className="w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          placeholder={placeholder}
        />
      </div>
    );
  }
}
