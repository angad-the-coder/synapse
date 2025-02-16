import fs from "fs";
import { H3Error, sendError } from "h3";


export default defineEventHandler(async (event) => {
  try {
    const start_date = getQuery(event)["start_date"] as string;
    const end_date = getQuery(event)?.["end_date"] as string | undefined;
    
    const query = {
      user_id: process.env.TERRA_USER_ID,
      start_date,
      to_webhook: false,
      with_samples: true
    } as Record<string, any>;
    if (end_date != null) {
      query.end_date = end_date;
    }

    // @ts-ignore
    const { data } = await $fetch(`${process.env.TERRA_BASE_URL}/daily`, {
      method: "GET",
      // @ts-ignore
      headers: {
        "x-api-key": process.env.TERRA_API_KEY,
        "dev-id": process.env.TERRA_DEV_ID,
      },
      query,
    });

    if (data.length === 0) {
      throw new Error("There is no stress data for this time period.")
    }
    return data![0].stress_data;

  } catch (error) {
    console.log(error);
    sendError(event, error as H3Error, false);
  }
});
