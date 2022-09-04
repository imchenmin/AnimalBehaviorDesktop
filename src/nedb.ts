const Datastore = require('nedb');

// 存放历史的实验记录的位置
const history_db = new Datastore({ filename: 'history.json', autoload: true });


export default {history_db}