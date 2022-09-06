var fs = require("fs");

/** 
 * @param csvfile {string} 表示文件路径的字符串
 * @returns data {Array}
 */
export function read_csv_line(csvfile: string): string[]{
  let csvstr: string = fs.readFileSync(csvfile,"utf8",'r+');
  let arr: string[] = csvstr.split('\n');
  let array: any = [];
  arr.forEach(line => {
    array.push(line.split(','));
  });
  return array
}