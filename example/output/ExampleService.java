package exp.data;

public interface ExampleService {

	@POST("/api/examples")
	Call<Example> createExample(@Body ExampleDto exampleDto);

	@GET("/api/examples-filtered/{testId}/{begin}/{end}/{status}/")
	Call<List<Example>> getAllExamplesFiltered(@Path("testId") Long testId, @Path("begin") String begin, @Path("end") String end, @Path("status") String status);

	@POST("/api/test")
	Call<Void> testExample(@Body ExampleDto exampleDto);

}