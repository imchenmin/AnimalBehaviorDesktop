<template >
    <div>
        编辑和存放实验组结构的地方。比如每一只动物对应的视频和组别。实验组，控制组。
        <vue-good-table :columns="columns" :rows="rows" :search-options="{
            enabled: true,
            trigger: 'enter',
            skipDiacritics: true,
            searchFn: mySearchFn,
            placeholder: 'Search this table',
        }"></vue-good-table>
    </div>
</template>
<script>
export default {
    name: 'ExperimentSetting',
    data() {
        return {
            columns: [
                {
                    label: 'Name',
                    field: 'name',
                },
                {
                    label: '分组',
                    field: 'group',
                    type: 'string',
                    filterOptions: {
                        styleClass: 'class1', // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: '选择列表', // placeholder for filter input
                        filterValue: '对照组', // initial populated value for this filter
                        filterDropdownItems: ['实验组','对照组'], // dropdown (with selected values) instead of text input
                        filterFn: this.columnFilterFn, //custom filter function that
                        trigger: 'enter', //only trigger on enter not on keyup 
                    },
                },
                {
                    label: 'Created On',
                    field: 'createdAt',
                    type: 'date',
                    dateInputFormat: 'yyyy-MM-dd',
                    dateOutputFormat: 'MMM do yy',
                },
                {
                    label: 'Percent',
                    field: 'score',
                    type: 'percentage',
                },
            ],
            rows: [
                { id: 1, name: "John", group: '实验组', createdAt: '2011-10-31', score: 0.03343 },
                { id: 2, name: "Jane", group: '实验组', createdAt: '2011-10-31', score: 0.03343 },
                { id: 3, name: "Susan", group: '实验组', createdAt: '2011-10-30', score: 0.03343 },
                { id: 4, name: "Chris", group: '实验组', createdAt: '2011-10-11', score: 0.03343 },
                { id: 5, name: "Dan", group: '实验组', createdAt: '2011-10-21', score: 0.03343 },
                { id: 6, name: "John", group: '实验组', createdAt: '2011-10-31', score: 0.03343 },
            ],
        }
    }
}
</script>
<style lang="">
    
</style>