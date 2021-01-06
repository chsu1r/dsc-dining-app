'use strict';

const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

exports.updateAvgRating = functions.database.ref('/users/{uid}/ratings').onWrite(async (change) => {
    const before_val = change.before.val();  // grab the state of the db before the change
    const after_val = change.after.val();  // grab the state of the db after the change

    var changed_hash = "";
    // search for the changed (or added) rating.
    for (const [food_hash, rating] of Object.entries(after_val)) {
        if (before_val && food_hash in before_val) {
            if (before_val[food_hash] !== after_val[food_hash]) { // change
                changed_hash = food_hash;
            }
        } else { // added
            changed_hash = food_hash;
        }
    }

    // if something has changed
    if (changed_hash !== "") {
        const foodDbRef = admin.database().ref("/food");
        const food_db_data = await foodDbRef.once('value');
        if (food_db_data.hasChild(changed_hash)) {  // if the food item that changed already exists in our global ratings
            const foodRef = admin.database().ref('/food/' + changed_hash);
            const food_data = await foodRef.once('value');
            const before_rating = food_data.val().avg_rating;
            const num_votes = food_data.val().num_votes;
            if (before_val && changed_hash in before_val) {  // if this is an existing user rating that was changed.
                // update the avg rating for food hash
                // i am 76% sure the math is correct idk i am not course 18
                const after_rating = before_rating - (before_val[changed_hash] / num_votes) + (after_val[changed_hash] / num_votes);
                admin.database().ref('/food/' + changed_hash).set({
                    avg_rating : after_rating,
                    num_votes : num_votes
                });
            } else {  // if this is a new user rating that was added.
                // add a vote to the running average.
                const after_rating = before_rating * (num_votes / (num_votes + 1)) + after_val[changed_hash] / (num_votes + 1);
                admin.database().ref('/food/' + changed_hash).set({
                    avg_rating : after_rating,
                    num_votes : num_votes + 1
                });
            }
        } else {
            // new entry in global ratings (first rating).
            admin.database().ref('/food/' + changed_hash).set({
                avg_rating : after_val[changed_hash],
                num_votes : 1
            });
        }
    }
    return null;
})
