const query = `
  query {
    modules (dept : "INFO"){
      edges {
        node {
          id
          name
        }
      }
    }
  }
`;

$.ajax({
  type: "GET",
  url: url_graphql,
  data: { query: query },
  success: function(response) {
    console.log(response);
  },
  error: function(error) {
    console.log(error);
  }
});