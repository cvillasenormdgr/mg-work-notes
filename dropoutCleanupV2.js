const createCsvWriter = require("csv-writer").createObjectCsvWriter;

const { firebaseApi, fetchFirebaseApi } = require("./services/firestore/index");
const { generateJWT } = require("./services/jwt");
const { FIREBASE_PROD_CREDENTIALS } = require("./services/firestore/config");
const firestoreParser = require("firestore-parser");

const main = async () => {
  const JWT_OBJECT = await generateJWT({
    firebaseConfig: FIREBASE_PROD_CREDENTIALS,
  });
  const ACCESS_TOKEN = JWT_OBJECT?.data?.access_token;

  let initialQuery = await fetchFirebaseApi({
    accessToken: ACCESS_TOKEN,
    projectId: FIREBASE_PROD_CREDENTIALS.projectId,
    body: {
      structuredQuery: {
        from: [
          {
            collectionId: "members",
          },
        ],
      },
    },
    method: "POST",
    urlExtend: ":runQuery",
  });

  const BATCH_SIZE = 5000;
  let batchedData = [];
  for (
    let counter = 0;
    counter < initialQuery.length;
    counter = counter + BATCH_SIZE
  )
    batchedData.push(initialQuery.slice(counter, counter + BATCH_SIZE));

  let allMemberDocuments = [];
  for (const batch of batchedData) {
    console.log(batch.length);
    const batchIds = batch
      ?.map((data) => {
        let id = data?.document?.name || "";
        if (id) {
          id = id.split("/");
          id = id[id.length - 1];
          return id;
        }
        return null;
      })
      .filter((batchId) => !!batchId);

    const batchRequest = await firebaseApi({
      accessToken: ACCESS_TOKEN,
      projectId: FIREBASE_PROD_CREDENTIALS.projectId,
    }).post(`:batchGet`, {
      documents: batchIds.map(
        (documentId) =>
          `projects/${FIREBASE_PROD_CREDENTIALS.projectId}/databases/(default)/documents/members/${documentId}`
      ),
    });

    console.log(batchRequest.data.slice(0, 2));

    let membersData = batchRequest?.data
      ?.map((member) => {
        let id = member?.found?.name;
        id = id.split("/");
        id = id[id.length - 1];
        if (!member.found.fields) return null;
        let memberDocument = firestoreParser(member?.found?.fields);
        memberDocument = { ...memberDocument, id };
        return memberDocument;
      })
      .filter((thing) => thing);
    allMemberDocuments.push(membersData);
  }

  allMemberDocuments = allMemberDocuments
    .flat()
    .sort((documentA, documentB) =>
      documentA?.finalPatientCode - documentB?.finalPatientCode ? 1 : -1
    );

  const allUniqueKeys = [];

  allMemberDocuments.forEach((document) =>
    Object.keys(document).forEach((key) => {
      if (!allUniqueKeys.includes(key)) allUniqueKeys.push(key);
    })
  );

  const csvWriter = createCsvWriter({
    path: "firestoreMembersCollection.csv",
    header: allUniqueKeys.map((key) => ({ id: key, title: key })),
  });

  csvWriter
    .writeRecords(allMemberDocuments)
    .then(() => console.log("CSV file written successfully"))
    .catch((err) => console.error("Error writing CSV file:", err))
};
main();