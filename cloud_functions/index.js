'use strict';

const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

// This is a listener for any changes made to a user ratings list. This function will execute any time a change is recorded.
// Here's what's happening:
// (1) We grab the state of the ratings list before and after the change.
// (2) We search for what changed by iterating across the final state of the ratings, comparing it to before.
//     - Note that this could either be an existing rating that was changed or a new rating.
// (3) If we find something was changed, then we grab a reference to the 'food' table, which has all our global ratings.
//     - If the 'food' table doesn't have the meal item that was changed, then we know this must be the first user rating.
//     - otherwise, we grab the existing rating and then recalculate the average. We do different math based on whether
//       this is a new or existing user rating to update the average.
// (4) In all cases, we "set" the new value by calling a ".set({new values})" call on the reference to the entry in the 'food' table.

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
            // new entry in global ratings (first user rating).
            admin.database().ref('/food/' + changed_hash).set({
                avg_rating : after_val[changed_hash],
                num_votes : 1
            });
        }
    }
    return null;
})
