import axios from "./api";
import { StrategyProps } from "../components/EditStrategy";

interface GetStrategyParamsResponse {
  success: boolean;
  data: StrategyProps | null;
  error?: string;
}


export type StrategyMetadata = {
    [key: string]: {
      label: string;
      params: {
        [param: string]: {
          type: string;
        };
      };
    };
  };
  

export async function getStrategyParams(): Promise<GetStrategyParamsResponse> {
  try {
    const result = await axios.get("/strategy-params");
    return {
      success: true,
      data: result.data,
    };
  } catch (error: any) {
    console.error("Error fetching strategy params:", error);
    return {
      success: false,
      data: null,
      error: error?.message ?? "Unknown error",
    };
  }
}

export async function testStrategy() {

}
