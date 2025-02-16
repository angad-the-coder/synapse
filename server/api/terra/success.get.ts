import fs from "fs";
import { H3Error, sendError } from "h3";

async function getStress(userId: string) {
  const endTime = new Date();
  const startTime = new Date(endTime.getTime() - 24 * 60 * 60 * 1000); // Last Day

  const data = await $fetch(`${process.env.TERRA_BASE_URL}/daily`, {
    method: "GET",
    // @ts-ignore
    headers: {
      "x-api-key": process.env.TERRA_API_KEY,
      "dev-id": process.env.TERRA_DEV_ID,
    },
    query: {
      user_id: userId,
      start_date: startTime.valueOf(),
      end_date: endTime.valueOf(),
      to_webhook: false,
      with_samples: true
    }
  })
  console.log(data);

  // Save response to file for debugging
  // fs.writeFileSync('../../../json/terra_response.json', JSON.stringify(data, null, 2));
}

export default defineEventHandler(async (event) => {
  try {
    const user_id = getQuery(event)["user_id"] as string;
    console.log(user_id);
    if (user_id == null) {
      throw new Error("No user connected. Please connect device first.");
    }

    await getStress(user_id);

    return "placeholder";
  } catch (error) {
    console.log(error);
    sendError(event, error as H3Error, false);
  }
});
