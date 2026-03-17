const airtable = require("airtable");

const main = async () => {
  const TARGET_TABLE = new airtable({
    apiKey:
      "",
  })
    .base("")
    .table("Members");

  const targetMembers = await TARGET_TABLE.select({
    filterByFormula: `{Dropout Date}`,
    view: "viwvgHTDOjyyuEGaF", // IT Filter 2
  }).all();

  for (const memberRecord of targetMembers) {
    console.log(
      await fetch(
        `https://asia-east2-medgrocer-28d8f.cloudfunctions.net/bestlife/deleteDocument?patientCode=${memberRecord.fields["Final Patient Code"]}`,
      ).then((res) => res.json()),
    );
  }
};

main();